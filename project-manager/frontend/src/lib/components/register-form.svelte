<script lang="ts">
	import {
		FieldGroup,
		Field,
		FieldLabel,
	} from "$lib/components/ui/field/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Eye, EyeOff, Loader2, ArrowRight } from "lucide-svelte";
	import { cn, type WithElementRef } from "$lib/utils.js";
	import type { HTMLFormAttributes } from "svelte/elements";
	import { authStore } from "$stores/auth";

	let {
		ref = $bindable(null),
		class: className,
		...restProps
	}: WithElementRef<HTMLFormAttributes> = $props();

	const id = $props.id();
	let showPassword = $state(false);
	let username = $state('');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let isLoading = $state(false);
	let errorMessage = $state('');

	async function handleSubmit(e: Event) {
		e.preventDefault();
		errorMessage = '';
		
		if (password !== confirmPassword) {
			errorMessage = 'Las contraseñas no coinciden';
			return;
		}

		if (password.length < 6) {
			errorMessage = 'La contraseña debe tener al menos 6 caracteres';
			return;
		}

		isLoading = true;

		try {
			await authStore.register(username, email, password);
			// Redirect to home on success
			window.location.href = '/tasklist';
		} catch (error: any) {
			errorMessage = error.message || 'Error al registrarse';
		} finally {
			isLoading = false;
		}
	}
</script>

<form class={cn("register-form", className)} bind:this={ref} {...restProps} onsubmit={handleSubmit}>
	{#if errorMessage}
		<div class="error-message">
			{errorMessage}
		</div>
	{/if}
	
	<FieldGroup>
		<Field>
			<FieldLabel for="username-{id}">Usuario</FieldLabel>
			<Input 
				id="username-{id}" 
				type="text" 
				placeholder="tu_usuario" 
				bind:value={username} 
				required 
				disabled={isLoading} 
				class="modern-input"
			/>
		</Field>

		<Field>
			<FieldLabel for="email-{id}">Correo electrónico</FieldLabel>
			<Input 
				id="email-{id}" 
				type="email" 
				placeholder="tu@email.com" 
				bind:value={email} 
				required 
				disabled={isLoading} 
				class="modern-input"
			/>
		</Field>
		
		<Field>
			<FieldLabel for="password-{id}">Contraseña</FieldLabel>
			<div class="password-wrapper">
				<Input 
					id="password-{id}" 
					type={showPassword ? 'text' : 'password'} 
					placeholder="Mínimo 6 caracteres"
					bind:value={password} 
					required 
					disabled={isLoading} 
					class="modern-input password-input"
				/>
				<button 
					type="button" 
					class="toggle-password"
					onclick={() => showPassword = !showPassword}
					aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
					disabled={isLoading}
				>
					{#if showPassword}
						<EyeOff size={18} />
					{:else}
						<Eye size={18} />
					{/if}
				</button>
			</div>
		</Field>

		<Field>
			<FieldLabel for="confirm-password-{id}">Confirmar contraseña</FieldLabel>
			<div class="password-wrapper">
				<Input 
					id="confirm-password-{id}" 
					type={showPassword ? 'text' : 'password'} 
					placeholder="Repite tu contraseña"
					bind:value={confirmPassword} 
					required 
					disabled={isLoading} 
					class="modern-input password-input"
				/>
			</div>
		</Field>
	</FieldGroup>
	
	<button type="submit" class="submit-btn" disabled={isLoading || !username || !email || !password || !confirmPassword}>
		{#if isLoading}
			<Loader2 size={20} class="animate-spin" />
			<span>Creando cuenta...</span>
		{:else}
			<span>Crear cuenta</span>
			<ArrowRight size={20} />
		{/if}
	</button>

	<div class="form-footer">
		<span class="footer-text">¿Ya tienes una cuenta?</span>
		<a href="/login" class="footer-link">Inicia sesión</a>
	</div>
</form>

<style>
	.register-form {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.error-message {
		padding: 1rem;
		background: rgba(252, 129, 129, 0.1);
		border: 1px solid rgba(252, 129, 129, 0.3);
		border-radius: 12px;
		color: #fc8181;
		font-size: 0.875rem;
		font-weight: 500;
		animation: shake 0.3s;
	}

	@keyframes shake {
		0%, 100% { transform: translateX(0); }
		25% { transform: translateX(-10px); }
		75% { transform: translateX(10px); }
	}

	.password-wrapper {
		position: relative;
		display: flex;
		align-items: center;
	}

	.toggle-password {
		position: absolute;
		right: 1rem;
		background: none;
		border: none;
		color: #7d8da6;
		cursor: pointer;
		padding: 0.5rem;
		display: flex;
		align-items: center;
		transition: color 0.3s;
		z-index: 10;
	}

	.toggle-password:hover:not(:disabled) {
		color: #ff7b54;
	}

	.toggle-password:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	:global(.modern-input) {
		background: rgba(15, 20, 36, 0.8) !important;
		border: 1.5px solid rgba(125, 141, 166, 0.2) !important;
		color: #f7fafc !important;
		border-radius: 14px !important;
		padding: 0.875rem 1.25rem !important;
		font-size: 0.9375rem !important;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
	}

	:global(.modern-input:focus) {
		border-color: rgba(255, 123, 84, 0.5) !important;
		box-shadow: 0 0 0 3px rgba(255, 123, 84, 0.1) !important;
		outline: none !important;
	}

	:global(.modern-input::placeholder) {
		color: rgba(125, 141, 166, 0.5) !important;
	}

	:global(.password-input) {
		padding-right: 3rem !important;
	}

	.submit-btn {
		width: 100%;
		height: 52px;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.75rem;
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		border: none;
		border-radius: 14px;
		color: #0a0e1a;
		font-size: 1rem;
		font-weight: 700;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		box-shadow: 0 8px 24px rgba(255, 123, 84, 0.3);
	}

	.submit-btn:hover:not(:disabled) {
		transform: translateY(-2px);
		box-shadow: 0 12px 32px rgba(255, 123, 84, 0.4);
	}

	.submit-btn:active:not(:disabled) {
		transform: translateY(0);
	}

	.submit-btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
		transform: none;
	}

	.form-footer {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		padding-top: 0.5rem;
	}

	.footer-text {
		color: #94a3b8;
		font-size: 0.9375rem;
	}

	.footer-link {
		color: #ff7b54;
		font-weight: 600;
		text-decoration: none;
		font-size: 0.9375rem;
		transition: color 0.3s;
	}

	.footer-link:hover {
		color: #ffb26b;
		text-decoration: underline;
	}
</style>

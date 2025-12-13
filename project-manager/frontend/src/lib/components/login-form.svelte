<script lang="ts">
	import {
		FieldGroup,
		Field,
		FieldLabel,
		FieldDescription,
		FieldSeparator,
	} from "$lib/components/ui/field/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Eye, EyeOff, Loader2, ArrowRight } from "lucide-svelte";
	import { cn, type WithElementRef } from "$lib/utils.js";
	import type { HTMLFormAttributes } from "svelte/elements";
	import { authStore } from "$stores/auth";
	import { goto } from '$app/navigation';

	let {
		ref = $bindable(null),
		class: className,
		...restProps
	}: WithElementRef<HTMLFormAttributes> = $props();

	const id = $props.id();
	let showPassword = $state(false);
	let email = $state('');
	let password = $state('');
	let isLoading = $state(false);
	let errorMessage = $state('');

	async function handleSubmit(e: Event) {
		e.preventDefault();
		errorMessage = '';
		isLoading = true;

		try {
			await authStore.login(email, password);
			// Redirigir usando goto de SvelteKit
			goto('/tasklist');
		} catch (error: any) {
			errorMessage = error.message || 'Error al iniciar sesión';
		} finally {
			isLoading = false;
		}
	}
</script>

<form class={cn("login-form", className)} bind:this={ref} {...restProps} onsubmit={handleSubmit}>
	{#if errorMessage}
		<div class="error-message">
			{errorMessage}
		</div>
	{/if}
	
	<FieldGroup>
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
			<div class="field-header">
				<FieldLabel for="password-{id}">Contraseña</FieldLabel>
				<a href="##" class="forgot-link">
					¿Olvidaste tu contraseña?
				</a>
			</div>
			<div class="password-wrapper">
				<Input 
					id="password-{id}" 
					type={showPassword ? 'text' : 'password'} 
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
	</FieldGroup>
	
	<button type="submit" class="submit-btn" disabled={isLoading || !email || !password}>
		{#if isLoading}
			<Loader2 size={20} class="animate-spin" />
			<span>Iniciando sesión...</span>
		{:else}
			<span>Iniciar sesión</span>
			<ArrowRight size={20} />
		{/if}
	</button>

	<div class="form-footer">
		<span class="footer-text">¿No tienes una cuenta?</span>
		<a href="/register" class="footer-link">Regístrate</a>
	</div>
</form>

<style>
	.login-form {
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
		text-align: center;
		animation: shake 0.4s ease;
	}

	@keyframes shake {
		0%, 100% { transform: translateX(0); }
		25% { transform: translateX(-10px); }
		75% { transform: translateX(10px); }
	}

	.field-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.5rem;
	}

	.forgot-link {
		font-size: 0.8125rem;
		color: #ff7b54;
		text-decoration: none;
		font-weight: 500;
		transition: all 0.2s ease;
	}

	.forgot-link:hover {
		color: #ffb26b;
		text-decoration: underline;
	}

	:global(.modern-input) {
		height: 48px !important;
		padding: 0 1.25rem !important;
		background: rgba(15, 20, 36, 0.8) !important;
		border: 1.5px solid rgba(125, 141, 166, 0.2) !important;
		border-radius: 14px !important;
		color: #f7fafc !important;
		font-size: 0.9375rem !important;
		transition: all 0.3s ease !important;
	}

	:global(.modern-input:focus) {
		border-color: rgba(255, 123, 84, 0.5) !important;
		box-shadow: 0 0 0 4px rgba(255, 123, 84, 0.1) !important;
		background: rgba(15, 20, 36, 1) !important;
	}

	:global(.modern-input::placeholder) {
		color: #4a5568 !important;
	}

	.password-wrapper {
		position: relative;
		display: flex;
		align-items: center;
	}

	:global(.password-input) {
		padding-right: 3rem !important;
	}

	.toggle-password {
		position: absolute;
		right: 1rem;
		background: none;
		border: none;
		color: #7d8da6;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0.5rem;
		border-radius: 8px;
		transition: all 0.2s ease;
	}

	.toggle-password:hover:not(:disabled) {
		color: #f7fafc;
		background: rgba(125, 141, 166, 0.1);
	}

	.toggle-password:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}

	.submit-btn {
		width: 100%;
		height: 52px;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.625rem;
		padding: 0 2rem;
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		border: none;
		border-radius: 14px;
		color: #0a0e1a;
		font-size: 1rem;
		font-weight: 700;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		box-shadow: 0 8px 24px rgba(255, 123, 84, 0.4);
		margin-top: 0.5rem;
	}

	.submit-btn:hover:not(:disabled) {
		transform: translateY(-2px);
		box-shadow: 0 12px 32px rgba(255, 123, 84, 0.6);
	}

	.submit-btn:active:not(:disabled) {
		transform: translateY(0);
	}

	.submit-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
		transform: none;
		box-shadow: 0 4px 16px rgba(255, 123, 84, 0.2);
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

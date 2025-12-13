<script lang="ts">
	import LoginForm from "$lib/components/login-form.svelte";
	import { Rocket, Sparkles } from "lucide-svelte";
</script>

<div class="login-container">
	<div class="login-left">
		<div class="login-content">
			<a href="/" class="brand-link">
				<div class="brand-icon">
					<Rocket size={20} />
				</div>
				<span class="brand-name">Project Manager</span>
			</a>
			
			<div class="login-form-wrapper">
				<div class="form-header">
					<h1 class="form-title">Bienvenido de nuevo</h1>
					<p class="form-subtitle">Inicia sesión para continuar con tus proyectos</p>
				</div>
				<LoginForm />
			</div>
		</div>
	</div>
	
	<div class="login-right">
		<div class="hero-content">
			<div class="floating-badge">
				<Sparkles size={16} />
				<span>Productividad redefinida</span>
			</div>
			
			<h2 class="hero-title">
				Gestiona tus proyectos
				<span class="gradient-text">de forma inteligente</span>
			</h2>
			
			<p class="hero-description">
				Organiza tareas, colabora con tu equipo y alcanza tus objetivos
				con nuestra plataforma moderna y eficiente.
			</p>
			
			<div class="stats-row">
				<div class="stat-item">
					<div class="stat-value">10k+</div>
					<div class="stat-label">Usuarios activos</div>
				</div>
				<div class="stat-item">
					<div class="stat-value">50k+</div>
					<div class="stat-label">Tareas completadas</div>
				</div>
				<div class="stat-item">
					<div class="stat-value">99%</div>
					<div class="stat-label">Satisfacción</div>
				</div>
			</div>
		</div>
		
		<div class="decorative-circles">
			<div class="circle circle-1"></div>
			<div class="circle circle-2"></div>
			<div class="circle circle-3"></div>
		</div>
	</div>
</div>

<style>
	.login-container {
		display: grid;
		grid-template-columns: 1fr 1fr;
		min-height: 100vh;
		background: linear-gradient(160deg, #0a0e1a 0%, #141b2e 100%);
	}

	.login-left {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 3rem;
		position: relative;
		z-index: 1;
	}

	.login-content {
		width: 100%;
		max-width: 440px;
		animation: fadeInLeft 0.6s ease-out;
	}

	@keyframes fadeInLeft {
		from {
			opacity: 0;
			transform: translateX(-30px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	.brand-link {
		display: inline-flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 3rem;
		text-decoration: none;
		transition: all 0.3s ease;
	}

	.brand-link:hover {
		transform: translateX(4px);
	}

	.brand-icon {
		width: 40px;
		height: 40px;
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #0a0e1a;
		box-shadow: 0 8px 24px rgba(255, 123, 84, 0.4);
	}

	.brand-name {
		font-size: 1.25rem;
		font-weight: 700;
		color: #f7fafc;
		letter-spacing: -0.01em;
	}

	.login-form-wrapper {
		background: rgba(20, 27, 46, 0.6);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 123, 84, 0.15);
		border-radius: 24px;
		padding: 2.5rem;
	}

	.form-header {
		margin-bottom: 2rem;
	}

	.form-title {
		font-size: 2rem;
		font-weight: 800;
		color: #f7fafc;
		margin-bottom: 0.5rem;
		letter-spacing: -0.02em;
	}

	.form-subtitle {
		color: #7d8da6;
		font-size: 0.9375rem;
	}

	.login-right {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 3rem;
		overflow: hidden;
	}

	.login-right::before {
		content: '';
		position: absolute;
		inset: 0;
		background: linear-gradient(135deg, rgba(255, 123, 84, 0.1), rgba(255, 178, 107, 0.05));
		z-index: 0;
	}

	.hero-content {
		position: relative;
		z-index: 1;
		max-width: 500px;
		animation: fadeInRight 0.6s ease-out;
	}

	@keyframes fadeInRight {
		from {
			opacity: 0;
			transform: translateX(30px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	.floating-badge {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.625rem 1.25rem;
		background: rgba(255, 123, 84, 0.15);
		border: 1px solid rgba(255, 123, 84, 0.3);
		border-radius: 50px;
		color: #ff7b54;
		font-size: 0.875rem;
		font-weight: 600;
		margin-bottom: 1.5rem;
		animation: float 3s ease-in-out infinite;
	}

	@keyframes float {
		0%, 100% { transform: translateY(0); }
		50% { transform: translateY(-10px); }
	}

	.hero-title {
		font-size: 3rem;
		font-weight: 800;
		line-height: 1.1;
		color: #f7fafc;
		margin-bottom: 1.5rem;
		letter-spacing: -0.02em;
	}

	.gradient-text {
		background: linear-gradient(120deg, #ff7b54, #ffb26b);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		display: block;
	}

	.hero-description {
		font-size: 1.125rem;
		color: #7d8da6;
		line-height: 1.6;
		margin-bottom: 3rem;
	}

	.stats-row {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 2rem;
	}

	.stat-item {
		text-align: center;
	}

	.stat-value {
		font-size: 2rem;
		font-weight: 800;
		background: linear-gradient(120deg, #ff7b54, #ffb26b);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		margin-bottom: 0.25rem;
	}

	.stat-label {
		font-size: 0.875rem;
		color: #7d8da6;
	}

	.decorative-circles {
		position: absolute;
		inset: 0;
		pointer-events: none;
		z-index: 0;
	}

	.circle {
		position: absolute;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(255, 123, 84, 0.1), transparent 70%);
	}

	.circle-1 {
		width: 400px;
		height: 400px;
		top: -100px;
		right: -100px;
		animation: float 15s ease-in-out infinite;
	}

	.circle-2 {
		width: 300px;
		height: 300px;
		bottom: -50px;
		left: -50px;
		animation: float 20s ease-in-out infinite reverse;
	}

	.circle-3 {
		width: 200px;
		height: 200px;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		animation: float 12s ease-in-out infinite;
	}

	@media (max-width: 1024px) {
		.login-container {
			grid-template-columns: 1fr;
		}

		.login-right {
			display: none;
		}

		.login-left {
			padding: 2rem 1.5rem;
		}
	}
</style>

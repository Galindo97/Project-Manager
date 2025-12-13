<script lang="ts">
	import RegisterForm from "$lib/components/register-form.svelte";
	import { Rocket, Sparkles, Users, Target, Zap } from "lucide-svelte";
</script>

<div class="register-container">
	<div class="register-left">
		<div class="register-content">
			<a href="/" class="brand-link">
				<div class="brand-icon">
					<Rocket size={20} />
				</div>
				<span class="brand-name">Project Manager</span>
			</a>
			
			<div class="register-form-wrapper">
				<div class="form-header">
					<h1 class="form-title">Crea tu cuenta</h1>
					<p class="form-subtitle">Únete y comienza a gestionar tus proyectos de manera eficiente</p>
				</div>
				<RegisterForm />
			</div>
		</div>
	</div>
	
	<div class="register-right">
		<div class="hero-content">
			<div class="floating-badge">
				<Sparkles size={16} />
				<span>Empieza gratis hoy</span>
			</div>
			
			<h2 class="hero-title">
				Todo lo que necesitas para
				<span class="gradient-text">alcanzar tus metas</span>
			</h2>
			
			<p class="hero-description">
				Únete a miles de usuarios que ya están transformando la manera
				en que gestionan sus proyectos y tareas.
			</p>
			
			<div class="features-list">
				<div class="feature-item">
					<div class="feature-icon">
						<Target size={20} />
					</div>
					<div class="feature-text">
						<h3>Organización total</h3>
						<p>Mantén todas tus tareas y proyectos en un solo lugar</p>
					</div>
				</div>
				<div class="feature-item">
					<div class="feature-icon">
						<Users size={20} />
					</div>
					<div class="feature-text">
						<h3>Colaboración fluida</h3>
						<p>Trabaja en equipo de manera eficiente y coordinada</p>
					</div>
				</div>
				<div class="feature-item">
					<div class="feature-icon">
						<Zap size={20} />
					</div>
					<div class="feature-text">
						<h3>Productividad máxima</h3>
						<p>Herramientas inteligentes que impulsan tu rendimiento</p>
					</div>
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
	.register-container {
		display: grid;
		grid-template-columns: 1fr 1fr;
		min-height: 100vh;
		background: linear-gradient(160deg, #0a0e1a 0%, #141b2e 100%);
	}

	.register-left {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 3rem;
		position: relative;
		z-index: 1;
	}

	.register-content {
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
		transition: transform 0.3s;
	}

	.brand-link:hover {
		transform: translateX(-4px);
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
	}

	.brand-name {
		font-size: 1.25rem;
		font-weight: 700;
		color: #f7fafc;
	}

	.register-form-wrapper {
		background: rgba(20, 27, 46, 0.6);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(125, 141, 166, 0.1);
		border-radius: 24px;
		padding: 2.5rem;
		box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
	}

	.form-header {
		margin-bottom: 2rem;
	}

	.form-title {
		font-size: 1.875rem;
		font-weight: 700;
		color: #f7fafc;
		margin-bottom: 0.5rem;
	}

	.form-subtitle {
		color: #94a3b8;
		font-size: 0.9375rem;
		line-height: 1.5;
	}

	/* Right side */
	.register-right {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 4rem;
		overflow: hidden;
		background: linear-gradient(135deg, rgba(255, 123, 84, 0.05) 0%, rgba(255, 178, 107, 0.05) 100%);
	}

	.hero-content {
		max-width: 500px;
		position: relative;
		z-index: 2;
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
		background: rgba(255, 123, 84, 0.1);
		border: 1px solid rgba(255, 123, 84, 0.3);
		border-radius: 50px;
		color: #ff7b54;
		font-size: 0.875rem;
		font-weight: 600;
		margin-bottom: 2rem;
		animation: float 3s ease-in-out infinite;
	}

	@keyframes float {
		0%, 100% { transform: translateY(0); }
		50% { transform: translateY(-10px); }
	}

	.hero-title {
		font-size: 2.5rem;
		font-weight: 800;
		line-height: 1.2;
		color: #f7fafc;
		margin-bottom: 1.5rem;
	}

	.gradient-text {
		display: block;
		background: linear-gradient(120deg, #ff7b54, #ffb26b);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.hero-description {
		color: #94a3b8;
		font-size: 1.125rem;
		line-height: 1.7;
		margin-bottom: 3rem;
	}

	.features-list {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.feature-item {
		display: flex;
		gap: 1rem;
		align-items: flex-start;
	}

	.feature-icon {
		width: 48px;
		height: 48px;
		background: rgba(255, 123, 84, 0.1);
		border: 1px solid rgba(255, 123, 84, 0.3);
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #ff7b54;
		flex-shrink: 0;
	}

	.feature-text h3 {
		font-size: 1rem;
		font-weight: 600;
		color: #f7fafc;
		margin-bottom: 0.25rem;
	}

	.feature-text p {
		font-size: 0.875rem;
		color: #94a3b8;
		line-height: 1.5;
	}

	.decorative-circles {
		position: absolute;
		inset: 0;
		overflow: hidden;
		opacity: 0.4;
	}

	.circle {
		position: absolute;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(255, 123, 84, 0.2) 0%, transparent 70%);
		animation: pulse 4s ease-in-out infinite;
	}

	.circle-1 {
		width: 400px;
		height: 400px;
		top: -100px;
		right: -100px;
		animation-delay: 0s;
	}

	.circle-2 {
		width: 300px;
		height: 300px;
		bottom: -50px;
		left: -50px;
		animation-delay: 1s;
	}

	.circle-3 {
		width: 200px;
		height: 200px;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		animation-delay: 2s;
	}

	@keyframes pulse {
		0%, 100% {
			transform: scale(1);
			opacity: 0.4;
		}
		50% {
			transform: scale(1.1);
			opacity: 0.6;
		}
	}

	@media (max-width: 1024px) {
		.register-container {
			grid-template-columns: 1fr;
		}

		.register-right {
			display: none;
		}

		.register-left {
			padding: 2rem;
		}
	}

	@media (max-width: 640px) {
		.register-form-wrapper {
			padding: 2rem 1.5rem;
		}

		.form-title {
			font-size: 1.5rem;
		}

		.form-subtitle {
			font-size: 0.875rem;
		}
	}
</style>

<script lang="ts">
	import { goto } from '$app/navigation';
	import { Rocket, CheckCircle2, Zap, Shield } from 'lucide-svelte';
</script>

<div class="home-container">
	<div class="hero-section">
		<div class="content-wrapper">
			<div class="hero-badge">
				<Rocket size={16} />
				<span>Gestiona tus proyectos con estilo</span>
			</div>
			
			<h1 class="hero-title">
				Organiza tu trabajo,
				<span class="gradient-text">alcanza tus metas</span>
			</h1>
			
			<p class="hero-subtitle">
				Una plataforma moderna y minimalista para gestionar tareas,
				proyectos y colaborar con tu equipo de forma eficiente.
			</p>
			
			<div class="cta-buttons">
				<button class="btn-primary" onclick={() => goto('/tasklist')}>
					Comenzar ahora
					<Zap size={18} />
				</button>
				<button class="btn-secondary" onclick={() => goto('/login')}>
					Iniciar sesión
				</button>
			</div>
			
			<div class="features-grid">
				<div class="feature-card">
					<div class="feature-icon">
						<CheckCircle2 size={24} />
					</div>
					<h3>Intuitivo</h3>
					<p>Interfaz limpia y fácil de usar</p>
				</div>
				
				<div class="feature-card">
					<div class="feature-icon">
						<Zap size={24} />
					</div>
					<h3>Rápido</h3>
					<p>Rendimiento optimizado</p>
				</div>
				
				<div class="feature-card">
					<div class="feature-icon">
						<Shield size={24} />
					</div>
					<h3>Seguro</h3>
					<p>Tus datos protegidos</p>
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	.home-container {
		min-height: 100vh;
		background: linear-gradient(160deg, #0a0e1a 0%, #141b2e 50%, #0f1420 100%);
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 2rem;
		position: relative;
		overflow: hidden;
	}

	.home-container::before {
		content: '';
		position: absolute;
		top: -50%;
		right: -20%;
		width: 800px;
		height: 800px;
		background: radial-gradient(circle, rgba(255, 123, 84, 0.15), transparent 70%);
		animation: float 20s ease-in-out infinite;
	}

	@keyframes float {
		0%, 100% { transform: translate(0, 0) scale(1); }
		50% { transform: translate(-100px, 100px) scale(1.1); }
	}

	.hero-section {
		max-width: 1200px;
		width: 100%;
		z-index: 1;
	}

	.content-wrapper {
		text-align: center;
		animation: fadeInUp 0.8s ease-out;
	}

	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(30px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.hero-badge {
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
		animation: slideIn 0.6s ease-out 0.2s both;
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateX(-20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	.hero-title {
		font-size: clamp(2.5rem, 8vw, 5rem);
		font-weight: 800;
		line-height: 1.1;
		margin-bottom: 1.5rem;
		color: #f7fafc;
		letter-spacing: -0.02em;
	}

	.gradient-text {
		background: linear-gradient(120deg, #ff7b54 0%, #ffb26b 50%, #ff9a5a 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		display: block;
	}

	.hero-subtitle {
		font-size: clamp(1rem, 2vw, 1.25rem);
		color: #7d8da6;
		max-width: 600px;
		margin: 0 auto 3rem;
		line-height: 1.6;
	}

	.cta-buttons {
		display: flex;
		gap: 1rem;
		justify-content: center;
		margin-bottom: 4rem;
		flex-wrap: wrap;
	}

	.btn-primary, .btn-secondary {
		padding: 1rem 2rem;
		border-radius: 16px;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		border: none;
	}

	.btn-primary {
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		color: #0a0e1a;
		box-shadow: 0 8px 30px rgba(255, 123, 84, 0.4);
	}

	.btn-primary:hover {
		transform: translateY(-3px);
		box-shadow: 0 12px 40px rgba(255, 123, 84, 0.6);
	}

	.btn-secondary {
		background: rgba(20, 27, 46, 0.8);
		color: #f7fafc;
		border: 1.5px solid rgba(125, 141, 166, 0.3);
		backdrop-filter: blur(10px);
	}

	.btn-secondary:hover {
		background: rgba(20, 27, 46, 1);
		border-color: rgba(255, 123, 84, 0.5);
		transform: translateY(-3px);
	}

	.features-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1.5rem;
		max-width: 900px;
		margin: 0 auto;
	}

	.feature-card {
		background: rgba(20, 27, 46, 0.6);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 123, 84, 0.1);
		border-radius: 20px;
		padding: 2rem;
		transition: all 0.3s ease;
		animation: fadeIn 0.6s ease-out both;
	}

	.feature-card:nth-child(1) { animation-delay: 0.4s; }
	.feature-card:nth-child(2) { animation-delay: 0.5s; }
	.feature-card:nth-child(3) { animation-delay: 0.6s; }

	@keyframes fadeIn {
		from { opacity: 0; transform: scale(0.9); }
		to { opacity: 1; transform: scale(1); }
	}

	.feature-card:hover {
		transform: translateY(-8px);
		border-color: rgba(255, 123, 84, 0.3);
		box-shadow: 0 20px 40px rgba(255, 123, 84, 0.15);
	}

	.feature-icon {
		width: 60px;
		height: 60px;
		background: linear-gradient(135deg, rgba(255, 123, 84, 0.15), rgba(255, 123, 84, 0.05));
		border-radius: 16px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #ff7b54;
		margin-bottom: 1rem;
	}

	.feature-card h3 {
		font-size: 1.25rem;
		font-weight: 700;
		color: #f7fafc;
		margin-bottom: 0.5rem;
	}

	.feature-card p {
		color: #7d8da6;
		font-size: 0.9375rem;
		line-height: 1.5;
	}

	@media (max-width: 768px) {
		.cta-buttons {
			flex-direction: column;
			align-items: stretch;
		}

		.btn-primary, .btn-secondary {
			width: 100%;
			justify-content: center;
		}
	}
</style>

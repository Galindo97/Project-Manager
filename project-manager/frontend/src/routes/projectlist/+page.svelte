<script lang="ts">
	import ProjectList from '$lib/ProjectList.svelte';
	import { Plus } from 'lucide-svelte';

	let projects = [
		{ id: 1, name: 'Rediseño Web', status: 'activo', description: 'Rediseñando el sitio web corporativo con nueva identidad.' },
		{ id: 2, name: 'App Móvil', status: 'activo', description: 'Desarrollando las aplicaciones móviles para iOS y Android.' },
		{ id: 3, name: 'Campaña de Marketing', status: 'completado', description: 'Planificación y ejecución de la campaña de marketing Q4.' },
		{ id: 4, name: 'Migración de Sistema', status: 'archivado', description: 'Migrando datos heredados a la nueva infraestructura en la nube.' }
	];

	function handleSelect(id: number) {
		console.log('Proyecto seleccionado', id);
	}
</script>

<div class="projectlist-page">
	<!-- Hero Section -->
	<div class="page-hero">
		<div class="hero-badge">
			<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
				<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
				<polyline points="22 4 12 14.01 9 11.01"/>
			</svg>
			<span>Gestión de Proyectos</span>
		</div>
		<h1 class="hero-title">
			<span class="title-gradient">Tus Proyectos</span>
			<span class="title-accent">en un solo lugar</span>
		</h1>
		<p class="hero-description">
			Organiza, supervisa y completa tus proyectos de manera eficiente con herramientas potentes y una interfaz intuitiva.
		</p>
		<button class="project-new-btn">
			<Plus class="mr-2 h-4 w-4" />
			Crear Nuevo Proyecto
		</button>
	</div>

	<!-- Stats Section -->
	<div class="stats-grid">
		<div class="stat-card">
			<div class="stat-icon active">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<circle cx="12" cy="12" r="10"/>
					<polyline points="12 6 12 12 16 14"/>
				</svg>
			</div>
			<div class="stat-content">
				<span class="stat-value">{projects.filter(p => p.status === 'activo').length}</span>
				<span class="stat-label">Proyectos Activos</span>
			</div>
		</div>

		<div class="stat-card">
			<div class="stat-icon completed">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<polyline points="20 6 9 17 4 12"/>
				</svg>
			</div>
			<div class="stat-content">
				<span class="stat-value">{projects.filter(p => p.status === 'completado').length}</span>
				<span class="stat-label">Completados</span>
			</div>
		</div>

		<div class="stat-card">
			<div class="stat-icon total">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
				</svg>
			</div>
			<div class="stat-content">
				<span class="stat-value">{projects.length}</span>
				<span class="stat-label">Total de Proyectos</span>
			</div>
		</div>
	</div>

	<!-- Projects Section -->
	<div class="projects-section">
		<div class="section-header">
			<h2 class="section-title">Todos los Proyectos</h2>
			<div class="section-filters">
				<button class="filter-btn active">Todos</button>
				<button class="filter-btn">Activos</button>
				<button class="filter-btn">Completados</button>
			</div>
		</div>
		<ProjectList {projects} onSelect={handleSelect} />
	</div>
</div>

<style>
	.projectlist-page {
		padding: 0;
		min-height: calc(100vh - 140px);
	}

	/* Hero Section */
	.page-hero {
		position: relative;
		padding: 3rem 2rem;
		text-align: center;
		background: linear-gradient(135deg, rgba(255, 123, 84, 0.1) 0%, rgba(255, 178, 107, 0.05) 100%);
		border-radius: 24px;
		margin-bottom: 2rem;
		overflow: hidden;
	}

	.page-hero::before {
		content: '';
		position: absolute;
		top: -50%;
		right: -10%;
		width: 300px;
		height: 300px;
		background: radial-gradient(circle, rgba(255, 123, 84, 0.15) 0%, transparent 70%);
		border-radius: 50%;
		animation: float 20s ease-in-out infinite;
	}

	.page-hero::after {
		content: '';
		position: absolute;
		bottom: -30%;
		left: -5%;
		width: 250px;
		height: 250px;
		background: radial-gradient(circle, rgba(255, 178, 107, 0.1) 0%, transparent 70%);
		border-radius: 50%;
		animation: float 15s ease-in-out infinite reverse;
	}

	@keyframes float {
		0%, 100% { transform: translate(0, 0) scale(1); }
		50% { transform: translate(20px, -20px) scale(1.1); }
	}

	.hero-badge {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		background: rgba(15, 20, 36, 0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 123, 84, 0.3);
		border-radius: 50px;
		color: #ff7b54;
		font-size: 0.875rem;
		font-weight: 600;
		margin-bottom: 1.5rem;
		position: relative;
		z-index: 1;
	}

	.hero-title {
		font-size: 3rem;
		font-weight: 800;
		line-height: 1.2;
		margin-bottom: 1rem;
		position: relative;
		z-index: 1;
	}

	.title-gradient {
		display: block;
		background: linear-gradient(120deg, #ff7b54, #ffb26b);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.title-accent {
		display: block;
		color: #94a3b8;
		font-weight: 600;
		font-size: 2rem;
	}

	.hero-description {
		max-width: 600px;
		margin: 0 auto 2rem;
		color: #94a3b8;
		font-size: 1.125rem;
		line-height: 1.6;
		position: relative;
		z-index: 1;
	}

	.project-new-btn {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		height: 52px;
		padding: 0 2rem;
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		border: none;
		border-radius: 16px;
		color: #0a0e1a;
		font-size: 1rem;
		font-weight: 700;
		box-shadow: 0 12px 32px rgba(255, 123, 84, 0.4);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		cursor: pointer;
		position: relative;
		z-index: 1;
	}

	.project-new-btn::before {
		content: '';
		position: absolute;
		inset: 0;
		border-radius: 16px;
		padding: 2px;
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		-webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
		-webkit-mask-composite: xor;
		mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
		mask-composite: exclude;
		opacity: 0;
		transition: opacity 0.3s;
	}

	.project-new-btn:hover {
		transform: translateY(-4px) scale(1.02);
		box-shadow: 0 16px 48px rgba(255, 123, 84, 0.6);
	}

	.project-new-btn:hover::before {
		opacity: 1;
	}

	.project-new-btn:active {
		transform: translateY(-2px) scale(1);
	}

	/* Stats Grid */
	.stats-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1.5rem;
		margin-bottom: 3rem;
	}

	.stat-card {
		position: relative;
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1.5rem;
		background: rgba(15, 20, 36, 0.8);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(125, 141, 166, 0.2);
		border-radius: 16px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		overflow: hidden;
	}

	.stat-card::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 3px;
		background: linear-gradient(90deg, #ff7b54, #ffb26b);
		opacity: 0;
		transition: opacity 0.3s;
	}

	.stat-card:hover {
		transform: translateY(-4px);
		border-color: rgba(255, 123, 84, 0.4);
		box-shadow: 0 12px 32px rgba(255, 123, 84, 0.2);
	}

	.stat-card:hover::before {
		opacity: 1;
	}

	.stat-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 48px;
		height: 48px;
		border-radius: 12px;
		flex-shrink: 0;
		position: relative;
	}

	.stat-icon::after {
		content: '';
		position: absolute;
		inset: -2px;
		border-radius: 12px;
		padding: 2px;
		background: linear-gradient(135deg, currentColor, transparent);
		-webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
		-webkit-mask-composite: xor;
		mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
		mask-composite: exclude;
		opacity: 0.3;
	}

	.stat-icon.active {
		background: rgba(255, 123, 84, 0.15);
		color: #ff7b54;
	}

	.stat-icon.completed {
		background: rgba(16, 185, 129, 0.15);
		color: #10b981;
	}

	.stat-icon.total {
		background: rgba(99, 179, 237, 0.15);
		color: #63b3ed;
	}

	.stat-content {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.stat-value {
		font-size: 2rem;
		font-weight: 700;
		color: #f7fafc;
		line-height: 1;
	}

	.stat-label {
		font-size: 0.875rem;
		color: #94a3b8;
		font-weight: 500;
	}

	/* Projects Section */
	.projects-section {
		margin-top: 2rem;
	}

	.section-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 2rem;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.section-title {
		font-size: 1.5rem;
		font-weight: 700;
		color: #f7fafc;
	}

	.section-filters {
		display: flex;
		gap: 0.5rem;
		background: rgba(15, 20, 36, 0.6);
		padding: 0.25rem;
		border-radius: 12px;
		border: 1px solid rgba(125, 141, 166, 0.2);
	}

	.filter-btn {
		padding: 0.5rem 1rem;
		background: transparent;
		border: none;
		border-radius: 8px;
		color: #94a3b8;
		font-size: 0.875rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s;
	}

	.filter-btn:hover {
		color: #f7fafc;
		background: rgba(125, 141, 166, 0.1);
	}

	.filter-btn.active {
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		color: #0a0e1a;
		box-shadow: 0 4px 12px rgba(255, 123, 84, 0.3);
	}

	/* Responsive */
	@media (max-width: 768px) {
		.page-hero {
			padding: 2rem 1rem;
		}

		.hero-title {
			font-size: 2rem;
		}

		.title-accent {
			font-size: 1.5rem;
		}

		.hero-description {
			font-size: 1rem;
		}

		.project-new-btn {
			width: 100%;
			justify-content: center;
		}

		.stats-grid {
			grid-template-columns: 1fr;
			gap: 0.75rem;
		}

		.projects-section {
			padding: 1.5rem;
		}

		.section-header {
			flex-direction: column;
			align-items: flex-start;
			gap: 1rem;
		}

		.section-filters {
			width: 100%;
			justify-content: space-between;
			gap: 0.5rem;
		}

		.filter-btn {
			flex: 1;
			font-size: 0.875rem;
		}
	}
</style>

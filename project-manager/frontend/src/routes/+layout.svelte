<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { page } from '$app/stores';

	let { children } = $props();
	
	// Rutas sin layout (login, home)
	let noLayoutRoutes = ['/login', '/'];
	let showLayout = $derived(!noLayoutRoutes.includes($page.url.pathname));

	// Títulos dinámicos por ruta
	const routeTitles: Record<string, string> = {
		'/tasklist': 'Mis Tareas',
		'/completed': 'Completadas',
		'/proyectos': 'Proyectos',
		'/projectlist': 'Proyectos',
		'/taskform': 'Nueva Tarea'
	};

	// Función para obtener el título basado en la ruta
	let pageTitle = $derived.by(() => {
		const pathname = $page.url.pathname;
		
		// Si es una ruta de tarea individual (/task/[id])
		if (pathname.startsWith('/task/')) {
			return 'Detalle de Tarea';
		}
		
		// Buscar título exacto
		return routeTitles[pathname] || 'Dashboard';
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if showLayout}
	<div class="app-layout">
		<Sidebar />
		<div class="main-wrapper">
			<header class="app-header">
				<div class="header-content">
					<h1 class="header-title">{pageTitle}</h1>
				</div>
			</header>
			<main class="app-main">
				{@render children()}
			</main>
		</div>
	</div>
{:else}
	{@render children()}
{/if}

<style>
	.app-layout {
		display: grid;
		grid-template-columns: 280px 1fr;
		min-height: 100vh;
		background: linear-gradient(160deg, #0a0e1a 0%, #141b2e 50%, #0f1420 100%);
	}

	.main-wrapper {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	.app-header {
		height: 70px;
		background: rgba(20, 27, 46, 0.6);
		backdrop-filter: blur(20px);
		border-bottom: 1px solid rgba(255, 123, 84, 0.1);
		display: flex;
		align-items: center;
		padding: 0 2rem;
		position: sticky;
		top: 0;
		z-index: 10;
	}

	.header-content {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.header-title {
		font-size: 1.25rem;
		font-weight: 700;
		background: linear-gradient(120deg, #ff7b54, #ffb26b);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		letter-spacing: -0.01em;
	}

	.app-main {
		flex: 1;
		padding: 2rem;
		overflow-y: auto;
	}

	@media (max-width: 1024px) {
		.app-layout {
			grid-template-columns: 1fr;
		}

		.app-header {
			padding: 0 1rem 0 4rem;
		}

		.app-main {
			padding: 1.5rem 1rem;
		}
	}
</style>

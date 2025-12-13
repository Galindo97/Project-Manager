<script lang="ts">
	import { page } from '$app/stores';
	import {
		LayoutDashboard,
		CheckSquare,
		CheckCircle,
		FolderKanban,
		LogOut,
		Rocket,
		Menu,
		X
	} from 'lucide-svelte';
	import { cn } from '$lib/utils';

	let currentPath = $derived($page.url.pathname);
	let isMobileMenuOpen = $state(false);

	const navItems = [
		{ href: '/projectlist', label: 'Proyectos', icon: LayoutDashboard },
		{ href: '/tasklist', label: 'Tareas', icon: CheckSquare },
		{ href: '/completed', label: 'Completadas', icon: CheckCircle },
		{ href: '/proyectos', label: 'Todos los proyectos', icon: FolderKanban }
	];

	function toggleMobileMenu() {
		isMobileMenuOpen = !isMobileMenuOpen;
	}

	function closeMobileMenu() {
		isMobileMenuOpen = false;
	}

	// Close menu when route changes
	$effect(() => {
		$page.url.pathname;
		closeMobileMenu();
	});
</script>

<!-- Mobile menu button -->
<button class="mobile-menu-btn" onclick={toggleMobileMenu} aria-label="Toggle menu">
	{#if isMobileMenuOpen}
		<X size={24} />
	{:else}
		<Menu size={24} />
	{/if}
</button>

<!-- Backdrop overlay for mobile -->
{#if isMobileMenuOpen}
	<button 
		class="mobile-backdrop" 
		onclick={closeMobileMenu}
		onkeydown={(e) => e.key === 'Enter' && closeMobileMenu()}
		aria-label="Close menu"
		tabindex="0"
	></button>
{/if}

<aside class="sidebar" class:open={isMobileMenuOpen}>
	<div class="sidebar-header">
		<a href="/" class="brand-link">
			<div class="brand-icon">
				<Rocket size={18} />
			</div>
			<span class="brand-name">Project Manager</span>
		</a>
	</div>
	
	<nav class="sidebar-nav">
		{#each navItems as item}
			<a
				href={item.href}
				class={cn(
					"nav-item",
					currentPath === item.href && "active"
				)}
			>
				<item.icon size={20} />
				<span>{item.label}</span>
			</a>
		{/each}
	</nav>
	
	<div class="sidebar-footer">
		<div class="user-card">
			<div class="user-avatar">
				<span>U</span>
			</div>
			<div class="user-info">
				<div class="user-name">Usuario</div>
				<div class="user-email">user@example.com</div>
			</div>
		</div>
		
		<button class="logout-btn" onclick={() => window.location.href = '/login'}>
			<LogOut size={18} />
			<span>Cerrar sesión</span>
		</button>
	</div>
</aside>

<style>
	.sidebar {
		width: 280px;
		height: 100vh;
		background: rgba(15, 20, 36, 0.95);
		backdrop-filter: blur(20px);
		border-right: 1px solid rgba(255, 123, 84, 0.1);
		display: flex;
		flex-direction: column;
		position: sticky;
		top: 0;
		overflow-y: auto;
	}

	.sidebar-header {
		padding: 1.5rem;
		border-bottom: 1px solid rgba(125, 141, 166, 0.1);
	}

	.brand-link {
		display: flex;
		align-items: center;
		gap: 0.875rem;
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
		box-shadow: 0 4px 16px rgba(255, 123, 84, 0.4);
	}

	.brand-name {
		font-size: 1.125rem;
		font-weight: 700;
		color: #f7fafc;
		letter-spacing: -0.01em;
	}

	.sidebar-nav {
		flex: 1;
		padding: 1.5rem 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.nav-item {
		display: flex;
		align-items: center;
		gap: 0.875rem;
		padding: 0.875rem 1.25rem;
		border-radius: 14px;
		color: #7d8da6;
		text-decoration: none;
		font-size: 0.9375rem;
		font-weight: 500;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		position: relative;
		overflow: hidden;
	}

	.nav-item::before {
		content: '';
		position: absolute;
		left: 0;
		top: 50%;
		transform: translateY(-50%);
		width: 3px;
		height: 0;
		background: linear-gradient(180deg, #ff7b54, #ffb26b);
		border-radius: 0 3px 3px 0;
		transition: height 0.3s ease;
	}

	.nav-item:hover {
		background: rgba(255, 123, 84, 0.08);
		color: #f7fafc;
		transform: translateX(4px);
	}

	.nav-item:hover::before {
		height: 60%;
	}

	.nav-item.active {
		background: rgba(255, 123, 84, 0.15);
		color: #ff7b54;
		font-weight: 600;
	}

	.nav-item.active::before {
		height: 80%;
	}

	.sidebar-footer {
		padding: 1.5rem 1rem;
		border-top: 1px solid rgba(125, 141, 166, 0.1);
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.user-card {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		background: rgba(255, 123, 84, 0.05);
		border-radius: 14px;
		border: 1px solid rgba(255, 123, 84, 0.1);
	}

	.user-avatar {
		width: 40px;
		height: 40px;
		border-radius: 50%;
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		display: flex;
		align-items: center;
		justify-content: center;
		color: #0a0e1a;
		font-weight: 700;
		font-size: 1rem;
	}

	.user-info {
		flex: 1;
		min-width: 0;
	}

	.user-name {
		font-size: 0.875rem;
		font-weight: 600;
		color: #f7fafc;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.user-email {
		font-size: 0.75rem;
		color: #7d8da6;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.logout-btn {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.625rem;
		padding: 0.875rem;
		background: rgba(252, 129, 129, 0.1);
		border: 1.5px solid rgba(252, 129, 129, 0.3);
		border-radius: 14px;
		color: #fc8181;
		font-size: 0.875rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.logout-btn:hover {
		background: rgba(252, 129, 129, 0.2);
		border-color: #fc8181;
		transform: translateY(-2px);
	}

	@media (max-width: 1024px) {
		.sidebar {
			position: fixed;
			left: -280px;
			top: 0;
			bottom: 0;
			z-index: 1000;
			transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		}

		.sidebar.open {
			left: 0;
		}
	}

	.mobile-menu-btn {
		display: none;
		position: fixed;
		top: 1rem;
		left: 1rem;
		z-index: 1001;
		width: 48px;
		height: 48px;
		border: none;
		background: rgba(20, 27, 46, 0.95);
		backdrop-filter: blur(20px);
		border-radius: 12px;
		color: #ff7b54;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
	}

	.mobile-menu-btn:hover {
		background: rgba(255, 123, 84, 0.15);
		transform: scale(1.05);
	}

	.mobile-backdrop {
		display: none;
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(4px);
		z-index: 999;
		animation: fadeIn 0.3s ease;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	@media (max-width: 1024px) {
		.mobile-menu-btn {
			display: flex;
			align-items: center;
			justify-content: center;
		}

		.mobile-backdrop {
			display: block;
		}
	}
</style>

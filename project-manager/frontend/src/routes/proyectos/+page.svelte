<script lang="ts">
	import { onMount } from 'svelte';
	import ProjectList from '$lib/ProjectList.svelte';
	import { Button } from "$lib/components/ui/button/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Label } from "$lib/components/ui/label/index.js";
	import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { Plus, Loader2 } from 'lucide-svelte';

	type Project = {
		id: number;
		name: string;
		description: string;
		status?: string;
	};

	let projects = $state<Project[]>([]);
	let isLoading = $state(true);
	let isCreating = $state(false);
	let open = $state(false);

	let name = $state('');
	let description = $state('');

	async function loadProjects() {
		isLoading = true;
		try {
			const res = await fetch('http://localhost:8000/projects');
			if (!res.ok) throw new Error('Error al obtener proyectos');
			projects = await res.json();
		} catch (error) {
			console.error('Error cargando proyectos:', error);
		} finally {
			isLoading = false;
		}
	}

	async function addProject() {
		if (!name.trim()) return;
		isCreating = true;
		try {
			const res = await fetch('http://localhost:8000/projects', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ name, description }),
			});
			if (res.ok) {
				const newProject = await res.json();
				projects = [...projects, newProject];
				name = '';
				description = '';
				open = false;
			}
		} catch (error) {
			console.error('Error creating project:', error);
		} finally {
			isCreating = false;
		}
	}

	async function deleteProject(id: number) {
		if (!confirm('¿Seguro que quieres eliminar este proyecto?')) return;
		try {
			const res = await fetch(`http://localhost:8000/projects/${id}`, {
				method: 'DELETE'
			});
			if (res.ok) {
				projects = projects.filter(p => p.id !== id);
			}
		} catch (error) {
			console.error('Error deleting project:', error);
		}
	}

	function handleSelect(id: number) {
		// Navigate to project details or something
		console.log('Selected', id);
	}

	onMount(() => {
		loadProjects();
	});
</script>

<div class="proyectos-page">
	<div class="flex items-center justify-between mb-8">
		<div class="space-y-1">
			<h2 class="text-3xl font-bold bg-linear-to-r from-[#ff7b54] to-[#ffb26b] bg-clip-text text-transparent">Proyectos</h2>
			<p class="text-sm text-[#94a3b8]">
				Gestiona tus proyectos activos.
			</p>
		</div>
		
		<Dialog.Root bind:open>
			<Dialog.Trigger>
				<button class="project-new-btn">
					<Plus class="mr-2 h-4 w-4" />
					Nuevo Proyecto
				</button>
			</Dialog.Trigger>
			<Dialog.Content class="sm:max-w-[425px]">
				<Dialog.Header>
					<Dialog.Title>Crear Proyecto</Dialog.Title>
					<Dialog.Description>
						Añade un nuevo proyecto a tu espacio de trabajo.
					</Dialog.Description>
				</Dialog.Header>
				<div class="grid gap-4 py-4">
					<div class="grid gap-2">
						<Label for="name">Nombre</Label>
						<Input id="name" bind:value={name} placeholder="Ej. Rediseño Web" />
					</div>
					<div class="grid gap-2">
						<Label for="description">Descripción</Label>
						<Input id="description" bind:value={description} placeholder="Breve descripción..." />
					</div>
				</div>
				<Dialog.Footer>
					<button type="submit" onclick={addProject} disabled={isCreating} class="dialog-submit-btn">
						{#if isCreating}
							<Loader2 class="mr-2 h-4 w-4 animate-spin" />
							<span>Creando...</span>
						{:else}
							<span>Crear Proyecto</span>
						{/if}
					</button>
				</Dialog.Footer>
			</Dialog.Content>
		</Dialog.Root>
	</div>

	{#if isLoading}
		<div class="flex h-40 items-center justify-center">
			<Loader2 class="h-8 w-8 animate-spin text-muted-foreground" />
		</div>
	{:else}
		<ProjectList {projects} onSelect={handleSelect} onDelete={deleteProject} />
	{/if}
</div>

<style>
	.proyectos-page {
		padding: 2rem 0;
	}

	.project-new-btn {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		height: 48px;
		padding: 0 1.5rem;
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		border: none;
		border-radius: 14px;
		color: #0a0e1a;
		font-size: 0.9375rem;
		font-weight: 700;
		box-shadow: 0 8px 24px rgba(255, 123, 84, 0.4);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		cursor: pointer;
	}

	.project-new-btn:hover {
		transform: translateY(-2px);
		box-shadow: 0 12px 32px rgba(255, 123, 84, 0.6);
	}

	.project-new-btn:active {
		transform: translateY(0);
	}

	.dialog-submit-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		width: 100%;
		height: 44px;
		padding: 0 1.5rem;
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		border: none;
		border-radius: 12px;
		color: #0a0e1a;
		font-size: 0.9375rem;
		font-weight: 700;
		box-shadow: 0 4px 12px rgba(255, 123, 84, 0.3);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		cursor: pointer;
	}

	.dialog-submit-btn:hover:not(:disabled) {
		transform: translateY(-2px);
		box-shadow: 0 8px 20px rgba(255, 123, 84, 0.5);
	}

	.dialog-submit-btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
		transform: none;
	}

	@media (max-width: 768px) {
		.proyectos-page {
			padding: 1rem 0;
		}

		.flex.items-center.justify-between {
			flex-direction: column;
			align-items: flex-start;
			gap: 1rem;
		}

		.project-new-btn {
			width: 100%;
			justify-content: center;
		}

		.space-y-1 h2 {
			font-size: 2rem;
		}
	}
</style>

<script lang="ts">
	import { Folder, ArrowRight, MoreHorizontal, Trash2 } from 'lucide-svelte';
	import { cn } from '$lib/utils';
	import { Button } from "$lib/components/ui/button/index.js";

	export let projects: any[] = [];
	export let onSelect: (id: number) => void;
	export let onDelete: ((id: number) => void) | undefined = undefined;
</script>

<div class="w-full project-list-wrapper">
	{#if projects.length === 0}
		<div class="empty-projects">
			<Folder class="mb-3 h-10 w-10 opacity-20" />
			<p class="text-sm font-medium">Aún no hay proyectos</p>
			<p class="text-xs text-[#94a3b8]">Crea un proyecto para comenzar</p>
		</div>
	{:else}
		<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
			{#each projects as project}
				<div class="relative group/card">
					<button
						class="project-card"
						onclick={() => onSelect(project.id)}
					>
						<div class="mb-4 flex w-full items-start justify-between">
							<div class="project-icon">
								<Folder class="h-5 w-5" />
							</div>
							<div class="project-status">
								{project.status || 'Activo'}
							</div>
						</div>
						
						<div class="space-y-2">
							<h3 class="project-title">
								{project.name}
							</h3>
							<p class="project-description">
								{project.description || 'Sin descripción.'}
							</p>
						</div>

						<div class="project-footer">
							<span>Ver Detalles</span>
							<ArrowRight class="h-4 w-4 transition-transform group-hover:translate-x-1" />
						</div>
					</button>
					{#if onDelete}
						<button 
							class="delete-project-btn"
							onclick={(e) => { e.stopPropagation(); onDelete && onDelete(project.id); }}
							title="Eliminar Proyecto"
						>
							<Trash2 class="h-4 w-4" />
						</button>
					{/if}
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.project-list-wrapper {
		margin-top: 1.5rem;
	}

	.empty-projects {
		display: flex;
		height: 10rem;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		border-radius: 1rem;
		border: 2px dashed rgba(125, 141, 166, 0.3);
		background: rgba(20, 27, 46, 0.4);
		backdrop-filter: blur(10px);
		color: #94a3b8;
	}

	.project-card {
		position: relative;
		display: flex;
		width: 100%;
		flex-direction: column;
		justify-content: space-between;
		overflow: hidden;
		border-radius: 1rem;
		background: rgba(15, 20, 36, 0.8);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(125, 141, 166, 0.2);
		padding: 1.5rem;
		text-align: left;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		cursor: pointer;
	}

	.project-card:hover {
		transform: translateY(-4px);
		box-shadow: 0 12px 32px rgba(255, 123, 84, 0.2);
		border-color: rgba(255, 123, 84, 0.4);
	}

	.project-card:active {
		transform: translateY(-2px) scale(0.99);
	}

	.project-icon {
		display: flex;
		height: 2.5rem;
		width: 2.5rem;
		align-items: center;
		justify-content: center;
		border-radius: 0.75rem;
		background: rgba(255, 123, 84, 0.15);
		color: #ff7b54;
		transition: all 0.3s;
	}

	.project-card:hover .project-icon {
		background: linear-gradient(135deg, #ff7b54, #ffb26b);
		color: #0a0e1a;
		transform: scale(1.1);
	}

	.project-status {
		border-radius: 9999px;
		background: rgba(125, 141, 166, 0.15);
		border: 1px solid rgba(125, 141, 166, 0.3);
		padding: 0.25rem 0.75rem;
		font-size: 0.75rem;
		font-weight: 500;
		color: #94a3b8;
	}

	.project-title {
		font-size: 1.125rem;
		font-weight: 600;
		color: #f7fafc;
		transition: color 0.3s;
		margin: 0;
	}

	.project-card:hover .project-title {
		color: #ff7b54;
	}

	.project-description {
		display: -webkit-box;
		-webkit-line-clamp: 2;
		line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
		font-size: 0.875rem;
		color: #94a3b8;
		line-height: 1.5;
		margin: 0;
	}

	.project-footer {
		margin-top: 1rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
		border-top: 1px solid rgba(125, 141, 166, 0.2);
		padding-top: 1rem;
		font-size: 0.75rem;
		color: #94a3b8;
	}

	.delete-project-btn {
		position: absolute;
		top: 1rem;
		right: 1rem;
		z-index: 10;
		border-radius: 9999px;
		background: rgba(252, 129, 129, 0.15);
		border: 1px solid rgba(252, 129, 129, 0.3);
		padding: 0.5rem;
		color: #fc8181;
		opacity: 0;
		transition: all 0.3s;
		cursor: pointer;
	}

	.group\/card:hover .delete-project-btn {
		opacity: 1;
	}

	.delete-project-btn:hover {
		background: rgba(252, 129, 129, 0.25);
		transform: scale(1.1);
	}

	@media (max-width: 768px) {
		.grid {
			grid-template-columns: 1fr !important;
		}

		.project-card {
			padding: 1.25rem;
		}

		.delete-project-btn {
			opacity: 1;
		}
	}
</style>

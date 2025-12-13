<script lang="ts">
	import { CheckCircle2, Circle, Clock, AlertCircle, FileText, Trash2, Pencil, Calendar, Paperclip } from 'lucide-svelte';
	import { cn } from '$lib/utils';
	import { Button } from "$lib/components/ui/button/index.js";

	export let tasks: any[] = [];
	export let onSelect: (id: number) => void;
	export let onToggleComplete: ((id: number) => void) | undefined = undefined;
	export let onDelete: ((id: number) => void) | undefined = undefined;
	export let onEdit: ((task: any) => void) | undefined = undefined;

	const priorityColors = {
		high: 'text-orange-400 bg-orange-500/10 border-orange-500/30',
		medium: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30',
		low: 'text-blue-400 bg-blue-500/10 border-blue-500/30'
	};

	const priorityLabels = {
		high: 'Alta',
		medium: 'Media',
		low: 'Baja'
	};
</script>

<div class="w-full space-y-4 task-list-wrapper">
	{#if tasks.length === 0}
		<div class="empty-tasks">
			<CheckCircle2 class="mb-3 h-10 w-10 opacity-20" />
			<p class="text-sm font-medium">No hay tareas</p>
			<p class="text-xs">Crea una tarea para comenzar</p>
		</div>
	{:else}
		<div class="grid gap-3">
			{#each tasks as task (task.id)}
				<div class="task-card">
					<!-- Main Content -->
					<button 
						class="task-main-content"
						onclick={() => onSelect(task.id)}
					>
						<div 
							role="button"
							tabindex="0"
							class="task-checkbox {task.completed ? 'completed' : ''}"
							onclick={(e) => { e.stopPropagation(); onToggleComplete && onToggleComplete(task.id); }}
							onkeydown={(e) => e.key === 'Enter' && onToggleComplete && onToggleComplete(task.id)}
						>
							<CheckCircle2 class="h-3.5 w-3.5" />
						</div>

						<div class="task-content">
							<div class="flex items-start justify-between gap-2">
								<span class="task-title {task.completed ? 'completed' : ''}">
									{task.title}
								</span>
							</div>
							
							<div class="task-metadata">
								{#if task.category}
									<span class="task-category">
										{task.category}
									</span>
								{/if}
								
								{#if task.deadline}
									<span class="task-deadline">
										<Calendar class="h-3 w-3" />
										{new Date(task.deadline).toLocaleDateString()}
									</span>
								{/if}

								{#if task.files && task.files.length > 0}
									<span class="task-files" title={`${task.files.length} archivos`}>
										<Paperclip class="h-3 w-3" />
										{task.files.length}
									</span>
								{/if}
							</div>
						</div>
					</button>

					<!-- Actions & Meta -->
					<div class="task-actions-wrapper">
						{#if task.priority}
							<span class="task-priority priority-{task.priority}">
								{priorityLabels[task.priority as keyof typeof priorityLabels] || task.priority}
							</span>
						{/if}

						<div class="task-actions">
							{#if onEdit}
								<Button variant="ghost" size="icon" class="h-8 w-8" onclick={() => onEdit && onEdit(task)}>
									<Pencil class="h-4 w-4" />
								</Button>
							{/if}
							{#if onDelete}
								<Button variant="ghost" size="icon" class="h-8 w-8 text-destructive hover:text-destructive" onclick={() => onDelete && onDelete(task.id)}>
									<Trash2 class="h-4 w-4" />
								</Button>
							{/if}
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.task-list-wrapper {
		margin-top: 1.5rem;
	}

	.empty-tasks {
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

	.task-card {
		position: relative;
		display: flex;
		width: 100%;
		align-items: center;
		gap: 1rem;
		overflow: hidden;
		border-radius: 1rem;
		background: rgba(15, 20, 36, 0.8);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(125, 141, 166, 0.2);
		padding: 1rem;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.task-card:hover {
		border-color: rgba(255, 123, 84, 0.4);
		box-shadow: 0 8px 24px rgba(255, 123, 84, 0.15);
		transform: translateY(-2px);
	}

	.task-main-content {
		display: flex;
		flex: 1;
		align-items: center;
		gap: 0.75rem;
		text-align: left;
		background: none;
		border: none;
		cursor: pointer;
		padding: 0;
	}

	.task-checkbox {
		display: flex;
		height: 1.25rem;
		width: 1.25rem;
		flex-shrink: 0;
		align-items: center;
		justify-content: center;
		border-radius: 9999px;
		border: 2px solid rgba(125, 141, 166, 0.3);
		color: transparent;
		transition: all 0.3s;
	}

	.task-checkbox:hover {
		border-color: rgba(255, 123, 84, 0.5);
	}

	.task-checkbox.completed {
		border-color: #ff7b54;
		background: #ff7b54;
		color: #0a0e1a;
	}

	.task-content {
		display: flex;
		flex: 1;
		flex-direction: column;
		gap: 0.375rem;
	}

	.task-title {
		font-weight: 500;
		line-height: 1.25;
		color: #f7fafc;
		transition: color 0.3s;
	}

	.task-title.completed {
		color: #94a3b8;
		text-decoration: line-through;
	}

	.task-metadata {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.75rem;
		color: #94a3b8;
	}

	.task-category {
		display: inline-flex;
		align-items: center;
		border-radius: 0.375rem;
		background: rgba(255, 178, 107, 0.15);
		border: 1px solid rgba(255, 178, 107, 0.3);
		padding: 0.125rem 0.5rem;
		font-weight: 500;
		color: #ffb26b;
	}

	.task-deadline,
	.task-files {
		display: flex;
		align-items: center;
		gap: 0.25rem;
	}

	.task-actions-wrapper {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.task-priority {
		display: inline-flex;
		align-items: center;
		border-radius: 9999px;
		border: 1px solid;
		padding: 0.25rem 0.625rem;
		font-size: 0.625rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.task-priority.priority-high {
		background: rgba(255, 123, 84, 0.15);
		border-color: rgba(255, 123, 84, 0.3);
		color: #ff7b54;
	}

	.task-priority.priority-medium {
		background: rgba(246, 224, 94, 0.15);
		border-color: rgba(246, 224, 94, 0.3);
		color: #f6e05e;
	}

	.task-priority.priority-low {
		background: rgba(99, 179, 237, 0.15);
		border-color: rgba(99, 179, 237, 0.3);
		color: #63b3ed;
	}

	.task-actions {
		display: flex;
		align-items: center;
		gap: 0.25rem;
		opacity: 0;
		transition: opacity 0.3s;
	}

	.task-card:hover .task-actions {
		opacity: 1;
	}
</style>

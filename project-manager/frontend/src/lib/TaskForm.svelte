
<script lang="ts">
import { Button } from "$lib/components/ui/button/index.js";
import { Input } from "$lib/components/ui/input/index.js";
import { Label } from "$lib/components/ui/label/index.js";
import { Loader2 } from 'lucide-svelte';

let title = $state('');
let priority = $state('medium');
let category = $state('');
let deadline = $state('');
let file = $state<File | null>(null);
let isSubmitting = $state(false);

let { onSubmit } = $props();

function handleFileChange(e: Event) {
	const target = e.target as HTMLInputElement;
	if (target.files && target.files.length > 0) {
		file = target.files[0];
	} else {
		file = null;
	}
}


async function handleSubmit(e: Event) {
	e.preventDefault();
	if (!title.trim()) return;
	isSubmitting = true;
	try {
		await onSubmit({
			title,
			priority,
			category,
			deadline,
			completed: false,
			file
		});
		// Reset form
		title = '';
		priority = 'medium';
		category = '';
		deadline = '';
		file = null;
	} finally {
		isSubmitting = false;
	}
}
</script>

<form onsubmit={handleSubmit} class="space-y-4" enctype="multipart/form-data">
   <div class="space-y-2">
	   <Label for="file">Archivo adjunto</Label>
	   <input id="file" type="file" onchange={handleFileChange} class="border rounded p-2 w-full" />
	   {#if file}
		   <div class="file-preview-container">
			   {#if file && file.type && file.type.startsWith('image/')}
				   <img src={URL.createObjectURL(file)} alt={file?.name || 'preview'} class="file-preview-img" />
			   {:else}
				   <span class="file-icon">📄</span>
			   {/if}
			   <div class="text-xs text-gray-500">{file?.name || ''}</div>
		   </div>
	   {/if}
   </div>
   <div class="space-y-2">
	   <Label for="title">Task Title</Label>
	   <Input id="title" bind:value={title} placeholder="What needs to be done?" required />
   </div>

   <div class="grid gap-4 sm:grid-cols-2">
	   <div class="space-y-2">
		   <Label for="priority">Priority</Label>
		   <select
			   id="priority"
			   bind:value={priority}
			   class="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
		   >
			   <option value="low">Low</option>
			   <option value="medium">Medium</option>
			   <option value="high">High</option>
		   </select>
	   </div>

	   <div class="space-y-2">
		   <Label for="category">Category</Label>
		   <Input id="category" bind:value={category} placeholder="Work, Personal, etc." />
	   </div>
   </div>

   <div class="space-y-2">
	   <Label for="deadline">Deadline</Label>
	   <Input id="deadline" type="date" bind:value={deadline} />
   </div>

   <Button type="submit" disabled={isSubmitting} class="w-full">
	   {#if isSubmitting}
		   <Loader2 class="mr-2 h-4 w-4 animate-spin" />
	   {/if}
	   Create Task
   </Button>
</form>

<style>
.file-preview-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.25rem;
}
.file-preview-img {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  background: #fff;
}
.file-icon {
  font-size: 2rem;
}
</style>

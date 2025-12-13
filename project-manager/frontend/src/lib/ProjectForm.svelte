<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Button } from "$lib/components/ui/button/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Label } from "$lib/components/ui/label/index.js";
	import { cn } from "$lib/utils.js";

	export let initial: any = {};
	const dispatch = createEventDispatcher();
	let name = initial.name || '';
	let description = initial.description || '';
	let status = initial.status || 'active';

	function submitForm() {
		dispatch('submit', { name, description, status });
	}
</script>

<form class="w-full max-w-lg space-y-6 rounded-xl border bg-card p-6 shadow-sm" onsubmit={(e) => { e.preventDefault(); submitForm(); }}>
	<div class="space-y-2">
		<h3 class="text-lg font-medium">Project Details</h3>
		<p class="text-sm text-muted-foreground">
			Enter the details for your project.
		</p>
	</div>

	<div class="space-y-4">
		<div class="space-y-2">
			<Label for="name">Name</Label>
			<Input id="name" type="text" bind:value={name} required placeholder="Project Name" />
		</div>

		<div class="space-y-2">
			<Label for="description">Description</Label>
			<textarea
				id="description"
				bind:value={description}
				class="flex min-h-20 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
				placeholder="Describe your project..."
			></textarea>
		</div>

		<div class="space-y-2">
			<Label for="status">Status</Label>
			<select
				id="status"
				bind:value={status}
				class="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
			>
				<option value="active">Active</option>
				<option value="archived">Archived</option>
				<option value="completed">Completed</option>
			</select>
		</div>
	</div>

	<div class="flex justify-end pt-4">
		<Button type="submit">Save Project</Button>
	</div>
</form>

<script>
	let projects = [];
	let name = '';
	let description = '';

	async function loadProjects() {
		try {
			const res = await fetch('https://br03lvnr-8000.usw3.devtunnels.ms/project');
			projects = await res.json();
		} catch (error) {
			console.error('Error cargando proyectos:', error);
		}
	}

	async function addProject() {
		if (!name.trim()) return alert('El nombre es obligatorio');

		const res = await fetch('https://br03lvnr-8000.usw3.devtunnels.ms/projects', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, description }),
		});

		if (res.ok) {
			name = '';
			description = '';
			loadProjects();
		} else {
			alert('Error al crear proyecto');
		}
	}

	loadProjects();
</script>

<h1>Gestor de Proyectos 🧩</h1>

<form on:submit|preventDefault={addProject}>
	<input placeholder="Nombre del proyecto" bind:value={name} required />
	<input placeholder="Descripción" bind:value={description} />
	<button type="submit">Agregar</button>
</form>

<hr />

{#if projects.length === 0}
	<p>No hay proyectos todavía...</p>
{:else}
	<ul>
		{#each projects as p}
			<li>{p.name} — {p.description}</li>
		{/each}
	</ul>
{/if}

<style>
	h1 {
		font-size: 1.5rem;
		margin-bottom: 1rem;
		color: #ffffff;
	}
	form {
		display: flex;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}
	input {
		padding: 0.5rem;
		border: 1px solid #ccc;
		border-radius: 5px;
	}
	button {
		padding: 0.5rem 1rem;
		background-color: #2563eb;
		color: white;
		border: none;
		border-radius: 5px;
		cursor: pointer;
	}
	button:hover {
		background-color: #1d4ed8;
	}
</style>

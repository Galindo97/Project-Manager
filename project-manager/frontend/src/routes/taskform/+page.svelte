<script lang="ts">
import TaskForm from '$lib/TaskForm.svelte';


let lastSubmission: any = null;



function handleSubmit(e: CustomEvent) {
  lastSubmission = e.detail;
  alert('Datos enviados: ' + JSON.stringify(e.detail));
}
</script>



<div class="space-y-6">
  
  
  <div class="max-w-2xl mx-auto">
    <div class="space-y-2 text-center">
      <h1 class="text-3xl font-bold tracking-tight">Nueva Tarea ✍️</h1>
      <p class="text-muted-foreground">Crea y organiza tus tareas de forma eficiente</p>
    </div>
    
    <div class="rounded-xl border bg-card text-card-foreground shadow p-6">
      <TaskForm onSubmit={handleSubmit} />
    </div>
    
    {#if lastSubmission}
      <div class="success-message">
        <div class="success-icon">✓</div>
        <div class="success-content">
          <h3>Tarea creada exitosamente</h3>
          <p>Última tarea: <strong>{lastSubmission.title || 'Sin título'}</strong></p>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}



.success-message {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(34, 197, 94, 0.1);
  border: 2px solid #22c55e;
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  animation: slideIn 0.4s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.success-icon {
  width: 48px;
  height: 48px;
  background: #22c55e;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.75rem;
  font-weight: 700;
  flex-shrink: 0;
}

.success-content {
  flex: 1;
}

.success-content h3 {
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
  color: #22c55e;
}

.success-content p {
  font-size: 0.95rem;
  color: #a1a1aa;
  margin: 0;
}

.success-content strong {
  color: #f3f3f3;
  font-weight: 600;
}


</style>
<script lang="ts">
  import { onMount } from 'svelte';
  import { slide, fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import { goto } from '$app/navigation';
  import * as AlertDialog from '$lib/components/ui/alert-dialog';
  import { CheckCircle2, Trash2, Calendar, RotateCcw, PartyPopper, Trophy, Award, Sun, Moon, Menu, X, Home, ListTodo, Flame, Clock, Search, XCircle, LogOut, Bot, Eye, Paperclip } from 'lucide-svelte';
  import { authStore } from '$lib/stores/auth';
  import ChatPanel from '$lib/ChatPanel.svelte';

  type Task = {
    id: number;
    title: string;
    priority: string;
    completed: boolean;
    category?: string;
    files?: string[];
    deadline?: string;
  };

  let completedTasks = $state<Task[]>([]);
  const API_URL = 'http://localhost:8000';
  let taskToDelete = $state<number | null>(null);
  let showDeleteDialog = $state(false);
  let darkMode = $state(false);
  
  let chatOpen = $state(false);
  let searchQuery = $state('');

  // Estadísticas
  let totalCompleted = $derived(completedTasks.length);
  let completedThisWeek = $derived(completedTasks.filter(t => {
    // Aquí podrías agregar lógica para filtrar por fecha de completado
    return true;
  }).length);

  // Tareas filtradas por búsqueda
  let filteredCompletedTasks = $derived(
    completedTasks.filter(t => 
      searchQuery === '' ||
      t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (t.category && t.category.toLowerCase().includes(searchQuery.toLowerCase()))
    )
  );

  async function fetchCompletedTasks() {
    const token = localStorage.getItem('access_token');
    const res = await fetch(`${API_URL}/tasks/completed`, {
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
        'Content-Type': 'application/json'
      }
    });
    if (!res.ok) {
      console.error('Error al obtener tareas completadas:', await res.text());
      completedTasks = [];
      return;
    }
    const allTasks = await res.json();
    console.log('TAREAS RECIBIDAS DEL BACKEND:', allTasks);
    // Normalizar el campo completed a booleano real
    function toBool(val: unknown): boolean {
      if (typeof val === 'boolean') return val;
      if (typeof val === 'string') return val.toLowerCase() === 'true' || val === '1';
      if (typeof val === 'number') return val === 1;
      return false;
    }
    const normalizedTasks = Array.isArray(allTasks) ? allTasks.map((t: Task) => ({
      ...t,
      completed: toBool(t.completed)
    })) : [];
    // Filtrar solo las completadas y ordenar por más recientes primero
    completedTasks = normalizedTasks.filter((t: Task) => t.completed);
  }

  async function restoreTask(id: number) {
    const task = completedTasks.find(t => t.id === id);
    if (!task) return;

    const token = localStorage.getItem('access_token');
    const body = {
      title: task.title,
      priority: task.priority,
      category: task.category || 'General',
      completed: false,
      ...(task.deadline ? { due_date: task.deadline } : {})
    };
    await fetch(`${API_URL}/tasks/${id}`, {
      method: 'PUT',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    await fetchCompletedTasks();
  }

  async function deleteTask() {
    if (taskToDelete === null) return;
    await fetch(`${API_URL}/tasks/${taskToDelete}`, { method: 'DELETE' });
    taskToDelete = null;
    await fetchCompletedTasks();
  }

  function openDeleteDialog(id: number) {
    taskToDelete = id;
    showDeleteDialog = true;
  }

  function getDeadlineText(deadline?: string) {
    if (!deadline) return null;
    const [year, month, day] = deadline.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });
  }

  onMount(() => {
    fetchCompletedTasks();
    
    const savedMode = localStorage.getItem('darkMode');
    darkMode = savedMode === 'true';
  });

  
</script>



<div class="completed-container" role="application">
  

  
    

  

  

  <!-- OVERLAY -->
  

  <div class="content-wrapper">
    <!-- Header con estadísticas -->
    <header class="header">
      <div class="header-content">
        <div class="title-section">
          <div class="title-with-icon">
            <Trophy size={32} strokeWidth={2.5} class="trophy-icon" />
            <h1>Tareas Completadas</h1>
          </div>
          <p class="subtitle">¡Celebra tus logros! 🎉</p>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <CheckCircle2 size={24} />
          </div>
          <div class="stat-content">
            <span class="stat-value">{totalCompleted}</span>
            <span class="stat-label">Total Completadas</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon award">
            <Award size={24} />
          </div>
          <div class="stat-content">
            <span class="stat-value">{completedThisWeek}</span>
            <span class="stat-label">Esta Semana</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon party">
            <PartyPopper size={24} />
          </div>
          <div class="stat-content">
            <span class="stat-value">{totalCompleted > 0 ? '100%' : '0%'}</span>
            <span class="stat-label">Tasa de Éxito</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Search Bar -->
    <div class="search-container">
      <div class="search-wrapper">
        <Search size={18} class="search-icon" />
        <input 
          type="text" 
          class="search-input"
          placeholder="Buscar tareas completadas por título o categoría..."
          bind:value={searchQuery}
        />
        {#if searchQuery}
          <button class="clear-search" onclick={() => searchQuery = ''} aria-label="Limpiar búsqueda">
            <XCircle size={16} />
          </button>
        {/if}
      </div>
    </div>

    <!-- Lista de tareas completadas -->
    <main class="main-content">
      {#if completedTasks.length === 0}
        <div class="empty-state" in:fade>
          <PartyPopper size={64} strokeWidth={1.5} />
          <h2>Aún no hay tareas completadas</h2>
          <p>Las tareas que completes aparecerán aquí</p>
          <a href="/tasklist" class="btn-primary">Ir a Tareas</a>
        </div>
      {:else if filteredCompletedTasks.length === 0}
        <div class="empty-state" in:fade>
          <Search size={64} strokeWidth={1.5} />
          <h2>No se encontraron tareas</h2>
          <p>Intenta con otros términos de búsqueda</p>
        </div>
      {:else}
        <div class="tasks-grid">
          {#each filteredCompletedTasks as task (task.id)}
            <div 
              class="completed-task-card priority-{task.priority}"
              transition:slide|local={{ duration: 300, easing: quintOut }}
              role="button"
              tabindex="0"
              onclick={() => goto(`/task/${task.id}`)}
              onkeydown={(e) => e.key === 'Enter' && goto(`/task/${task.id}`)}
            >
              <div class="task-header">
                <div class="task-check">
                  <CheckCircle2 size={24} strokeWidth={2.5} class="check-icon" />
                </div>
                <div class="task-info">
                  <h3 class="task-title">{task.title}</h3>
                  <div class="task-meta">
                    <span class="badge priority-{task.priority}">{task.priority}</span>
                    <span class="badge category">{task.category || 'General'}</span>
                    {#if task.deadline}
                      <span class="badge deadline">
                        <Calendar size={10} />
                        {getDeadlineText(task.deadline)}
                      </span>
                    {/if}
                  </div>
                </div>
                <div class="view-indicator">
                  <Eye size={18} />
                </div>
              </div>
              
              {#if task.files && task.files.length > 0}
                <div class="task-files-list">
                  {#each task.files as file}
                    <a
                      href={`http://localhost:8000/static/${file}`}
                      target="_blank"
                      rel="noopener"
                      class="file-container"
                      title={file}
                      onclick={(e) => e.stopPropagation()}
                    >
                      {#if file.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i)}
                        <img src={`http://localhost:8000/static/${file}`} alt={file} class="file-preview-img" />
                      {:else}
                        <Paperclip class="h-4 w-4" />
                      {/if}
                      <span class="file-name">{file}</span>
                    </a>
                  {/each}
                </div>
              {/if}
              <div class="task-actions">
                <button 
                  class="action-btn restore-btn" 
                  onclick={(e) => { e.stopPropagation(); restoreTask(task.id); }}
                  title="Restaurar tarea"
                >
                  <RotateCcw size={16} />
                  <span>Restaurar</span>
                </button>
                <button 
                  class="action-btn delete-btn" 
                  onclick={(e) => { e.stopPropagation(); openDeleteDialog(task.id); }}
                  title="Eliminar permanentemente"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            <style>
              .task-files-list {
                display: flex;
                gap: 0.5rem;
                margin-top: 0.5rem;
                margin-bottom: 0.5rem;
              }
              .file-container {
                display: inline-flex;
                align-items: center;
                gap: 0.25rem;
                background: rgba(99, 102, 241, 0.13);
                color: #6366f1;
                border-radius: 6px;
                padding: 0.1rem 0.6rem 0.1rem 0.3rem;
                font-size: 0.85rem;
                font-weight: 500;
                text-decoration: none;
                transition: background 0.2s;
                max-width: 160px;
                overflow: hidden;
              }
              .file-container:hover {
                background: rgba(99, 102, 241, 0.25);
                color: #4338ca;
              }
              .file-name {
                max-width: 90px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
              }
              .file-preview-img {
                width: 28px;
                height: 28px;
                object-fit: cover;
                border-radius: 4px;
                margin-right: 0.25rem;
                background: #fff;
                border: 1px solid #e5e7eb;
              }
            </style>
            </div>
          {/each}
        </div>
      {/if}
    </main>
  </div>
</div>

<!-- Alert Dialog para confirmar eliminación -->
<AlertDialog.Root bind:open={showDeleteDialog}>
  <AlertDialog.Content>
    <AlertDialog.Header>
      <AlertDialog.Title>¿Eliminar permanentemente?</AlertDialog.Title>
      <AlertDialog.Description>
        Esta acción no se puede deshacer. La tarea será eliminada de forma permanente.
      </AlertDialog.Description>
    </AlertDialog.Header>
    <AlertDialog.Footer>
      <AlertDialog.Cancel>Cancelar</AlertDialog.Cancel>
      <AlertDialog.Action onclick={() => { deleteTask(); showDeleteDialog = false; }}>Eliminar</AlertDialog.Action>
    </AlertDialog.Footer>
  </AlertDialog.Content>
</AlertDialog.Root>

<!-- FLOATING AI BUTTON -->
<button 
  class="floating-ai-btn" 
  onclick={() => chatOpen = true}
  aria-label="Abrir AI Assistant"
>
  <Bot size={24} />
</button>

<!-- AI CHAT PANEL -->
<ChatPanel bind:isOpen={chatOpen} {darkMode} />

<style>
  /* Reset y variables globales */
  :global(body) {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
  }

  .completed-container {
    min-height: 100vh;
    background: linear-gradient(160deg, #0a0e1a, #141b2e, #0f1420);
    position: relative;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  /* Layout principal */
  .content-wrapper {
    position: relative;
    z-index: 1;
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  /* Header */
  .header {
    margin-bottom: 2rem;
  }

  .header-content {
    margin-bottom: 2rem;
  }

  .title-section {
    flex: 1;
  }



  .title-with-icon {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
  }

  .title-with-icon :global(.trophy-icon) {
    color: #fbbf24;
    filter: drop-shadow(0 4px 12px rgba(251, 191, 36, 0.4));
  }

  h1 {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(120deg, #ff7b54, #ffb26b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    text-shadow: 0 2px 20px rgba(255, 123, 84, 0.3);
  }

  .subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    margin: 0;
  }

  /* Stats Grid */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .stat-card {
    background: rgba(20, 27, 46, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(125, 141, 166, 0.15);
    border-radius: 16px;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: linear-gradient(135deg, #ff7b54, #ffb26b);
    color: #0a0e1a;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(255, 123, 84, 0.3);
  }

  .stat-icon.award {
    background: linear-gradient(135deg, #f6e05e, #ecc94b);
  }

  .stat-icon.party {
    background: linear-gradient(135deg, #ffb26b, #ff7b54);
  }

  .stat-content {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .stat-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #f7fafc;
  }

  .stat-label {
    font-size: 0.875rem;
    color: #94a3b8;
  }

  /* Search Bar */
  .search-container {
    margin-bottom: 1.5rem;
  }

  .search-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-wrapper :global(.search-icon) {
    position: absolute;
    left: 1rem;
    color: #64748b;
    pointer-events: none;
    color: #7d8da6;
  }

  .search-input {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.75rem;
    border: 1.5px solid rgba(125, 141, 166, 0.2);
    border-radius: 14px;
    background: rgba(15, 20, 36, 0.8);
    color: #f7fafc;
    font-size: 0.9375rem;
    transition: all 0.3s;
  }

  .search-input:focus {
    outline: none;
    border-color: rgba(255, 123, 84, 0.5);
    box-shadow: 0 0 0 4px rgba(255, 123, 84, 0.1);
    background: rgba(15, 20, 36, 1);
  }

  .search-input::placeholder {
    color: #4a5568;
  }

  .clear-search {
    position: absolute;
    right: 1rem;
    background: none;
    border: none;
    cursor: pointer;
    color: #7d8da6;
    padding: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s;
  }

  .clear-search:hover {
    background: rgba(125, 141, 166, 0.1);
    color: #f7fafc;
  }

  /* Main Content */
  .main-content {
    background: rgba(20, 27, 46, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(125, 141, 166, 0.15);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    min-height: 400px;
  }

  /* Empty State */
  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #94a3b8;
  }

  .empty-state :global(svg) {
    color: #ff7b54;
    margin-bottom: 1.5rem;
  }

  .empty-state h2 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: #f7fafc;
  }

  .empty-state p {
    margin-bottom: 2rem;
    color: #94a3b8;
  }

  .btn-primary {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #ff7b54, #ffb26b);
    color: #0a0e1a;
    border-radius: 14px;
    text-decoration: none;
    font-weight: 700;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 8px 24px rgba(255, 123, 84, 0.4);
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(255, 123, 84, 0.6);
  }

  /* Tasks Grid */
  .tasks-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
  }

  .completed-task-card {
    background: rgba(15, 20, 36, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(125, 141, 166, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    border-left: 4px solid #ff7b54;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
  }

  .completed-task-card.priority-high {
    border-left-color: #ff7b54;
  }

  .completed-task-card.priority-medium {
    border-left-color: #f6e05e;
  }

  .completed-task-card.priority-low {
    border-left-color: #63b3ed;
  }

  .completed-task-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
  }

  .task-header {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    position: relative;
  }

  .task-check {
    flex-shrink: 0;
  }

  .task-check :global(.check-icon) {
    color: #ff7b54;
  }

  .task-info {
    flex: 1;
    min-width: 0;
  }

  .view-indicator {
    position: absolute;
    top: -0.5rem;
    right: -0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ff7b54;
    background: none;
    border-radius: 0;
    width: auto;
    height: auto;
    opacity: 0;
    transition: all 0.3s;
  }

  .completed-task-card:hover .view-indicator {
    opacity: 1;
    transform: scale(1.1);
  }

  .task-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f7fafc;
    margin: 0 0 0.75rem 0;
    text-decoration: line-through;
    opacity: 0.7;
  }

  .task-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: capitalize;
  }

  .badge.priority-high {
    background: rgba(255, 123, 84, 0.15);
    color: #ff7b54;
    border: 1px solid rgba(255, 123, 84, 0.3);
  }

  .badge.priority-medium {
    background: rgba(246, 224, 94, 0.15);
    color: #f6e05e;
    border: 1px solid rgba(246, 224, 94, 0.3);
  }

  .badge.priority-low {
    background: rgba(99, 179, 237, 0.15);
    color: #63b3ed;
    border: 1px solid rgba(99, 179, 237, 0.3);
  }

  .badge.category {
    background: rgba(255, 178, 107, 0.15);
    color: #ffb26b;
    border: 1px solid rgba(255, 178, 107, 0.3);
  }

  .badge.deadline {
    background: rgba(148, 163, 184, 0.15);
    color: #94a3b8;
    border: 1px solid rgba(148, 163, 184, 0.3);
  }

  .task-actions {
    display: flex;
    gap: 0.5rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(125, 141, 166, 0.2);
  }

  .action-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .restore-btn {
    background: rgba(255, 123, 84, 0.15);
    color: #ff7b54;
    border: 1px solid rgba(255, 123, 84, 0.3);
  }

  .restore-btn:hover {
    background: rgba(255, 123, 84, 0.25);
    transform: scale(1.02);
  }

  .delete-btn {
    background: rgba(252, 129, 129, 0.15);
    color: #fc8181;
    border: 1px solid rgba(252, 129, 129, 0.3);
    flex: 0 0 auto;
    padding: 0.5rem;
  }

  .delete-btn:hover {
    background: rgba(252, 129, 129, 0.25);
    transform: scale(1.05);
  }

  /* Responsive */
  @media (max-width: 1024px) {
    .title-with-icon {
      justify-content: center;
      width: 100%;
    }

    .title-section {
      text-align: center;
    }
  }

  @media (max-width: 768px) {
    .content-wrapper {
      padding: 1rem 0.75rem;
    }

    .toggle-mode {
      top: 0.75rem;
      right: 0.75rem;
      width: 32px;
      height: 32px;
    }

    .title-with-icon {
      gap: 0.75rem;
    }

    .title-with-icon :global(.trophy-icon) {
      width: 24px;
      height: 24px;
    }

    h1 {
      font-size: 1.5rem;
    }

    .subtitle {
      font-size: 0.95rem;
    }

    .header {
      margin-bottom: 1.5rem;
    }

    .header-content {
      margin-bottom: 1.5rem;
    }

    .stats-grid {
      grid-template-columns: 1fr;
      gap: 0.75rem;
    }

    .stat-card {
      padding: 1rem;
    }

    .stat-icon {
      width: 40px;
      height: 40px;
    }

    .stat-value {
      font-size: 1.5rem;
    }

    .stat-label {
      font-size: 0.8rem;
    }

    .main-content {
      padding: 1.25rem;
      border-radius: 16px;
    }

    .tasks-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .completed-task-card {
      padding: 1.25rem;
    }

    .task-title {
      font-size: 1rem;
    }

    .badge {
      font-size: 0.7rem;
      padding: 0.2rem 0.6rem;
    }

    .action-btn {
      font-size: 0.8rem;
      padding: 0.4rem 0.8rem;
    }

    .empty-state {
      padding: 3rem 1.5rem;
    }

    .empty-state :global(svg) {
      width: 48px;
      height: 48px;
    }

    .empty-state h2 {
      font-size: 1.25rem;
    }

    .empty-state p {
      font-size: 0.9rem;
    }
  }

  @media (max-width: 480px) {
    .content-wrapper {
      padding: 0.5rem;
    }

    h1 {
      font-size: 1.35rem;
    }

    .subtitle {
      font-size: 0.85rem;
    }

    .stats-grid {
      gap: 0.5rem;
    }

    .stat-card {
      padding: 0.875rem;
    }

    .main-content {
      padding: 1rem;
    }

    .completed-task-card {
      padding: 1rem;
    }

    .task-actions {
      flex-direction: column;
    }

    .action-btn {
      width: 100%;
    }

    .delete-btn {
      width: 100%;
    }
  }

  /* --- SIDEBAR --- */
  .menu-btn {
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 50;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: all 0.3s;
    color: #1e293b;
  }

  .app.dark .menu-btn {
    color: white;
  }

  .menu-btn:hover {
    background: rgba(255,255,255,0.3);
    transform: scale(1.05);
  }

  .sidebar {
    position: fixed;
    top: 0;
    left: -280px;
    width: 280px;
    height: 100vh;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 0, 0, 0.1);
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.1);
    z-index: 100;
    transition: left 0.3s ease;
    display: flex;
    flex-direction: column;
  }

  .app.dark .sidebar {
    background: rgba(0, 0, 0, 0.9);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.5);
  }

  .sidebar.open {
    left: 0;
  }

  .close-sidebar {
    background: none;
    border: none;
    cursor: pointer;
    color: #64748b;
    padding: 0.5rem;
    border-radius: 8px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .app.dark .close-sidebar {
    color: #94a3b8;
  }

  .close-sidebar:hover {
    background: rgba(0, 0, 0, 0.05);
    color: #1e293b;
  }

  .app.dark .close-sidebar:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }

  .sidebar-nav {
    flex: 1;
    padding: 1rem 0.75rem;
    overflow-y: auto;
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.875rem 1rem;
    margin-bottom: 0.5rem;
    border-radius: 12px;
    text-decoration: none;
    color: #64748b;
    font-weight: 500;
    transition: all 0.2s;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
    cursor: pointer;
    font-size: 0.95rem;
  }

  .app.dark .nav-item {
    color: #94a3b8;
  }

  .nav-item:hover {
    background: rgba(124, 58, 237, 0.1);
    color: #7c3aed;
  }

  .app.dark .nav-item:hover {
    background: rgba(167, 139, 250, 0.15);
    color: #a78bfa;
  }

  .nav-item.active {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white !important;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  }

  .app.dark .nav-item.active {
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    color: white !important;
  }

  .nav-item.active:hover {
    color: white !important;
  }

  .app.dark .nav-item.active:hover {
    color: white !important;
  }

  .logout-btn {
    margin-top: 0;
    color: #ef4444 !important;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 12px !important;
    padding: 0.875rem 1rem !important;
    margin-bottom: 1rem;
  }

  .app.dark .logout-btn {
    color: #f87171 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .logout-btn:hover {
    background: rgba(239, 68, 68, 0.1) !important;
    color: #dc2626 !important;
  }

  .app.dark .logout-btn:hover {
    background: rgba(248, 113, 113, 0.15) !important;
    color: #fca5a5 !important;
  }

  .sidebar-footer {
    padding: 1.25rem;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
  }

  .app.dark .sidebar-footer {
    border-top-color: rgba(255, 255, 255, 0.1);
  }

  .sidebar-stats {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }



  .sidebar-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 99;
    cursor: pointer;
  }

  /* --- FLOATING AI BUTTON --- */
  .floating-ai-btn {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff7b54, #ffb26b);
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #0a0e1a;
    box-shadow: 0 8px 24px rgba(255, 123, 84, 0.4);
    z-index: 1000;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .floating-ai-btn:hover {
    transform: scale(1.15) rotate(10deg);
    box-shadow: 0 12px 32px rgba(255, 123, 84, 0.6);
  }

  .floating-ai-btn:active {
    transform: scale(0.95);
  }

  @media (max-width: 768px) {
    .sidebar {
      width: 260px;
      left: -260px;
    }

    .menu-btn {
      top: 0.75rem;
      left: 0.75rem;
      width: 32px;
      height: 32px;
    }
    
    .floating-ai-btn {
      bottom: 1rem;
      right: 1rem;
      width: 56px;
      height: 56px;
    }
  }
</style>

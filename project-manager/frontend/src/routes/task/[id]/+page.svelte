<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { fade, slide, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import { 
    ArrowLeft, 
    Calendar, 
    Clock, 
    Paperclip, 
    FileText, 
    CheckCircle2, 
    AlertTriangle,
    Pencil,
    Save,
    X,
    Plus,
    Trash2,
    Image as ImageIcon,
    File as FileIcon,
    Video,
    Sun,
    Moon,
    Menu,
    Home,
    Award,
    LogOut,
    Bot
  } from 'lucide-svelte';
  import { authStore } from '$lib/stores/auth';
  import ChatPanel from '$lib/ChatPanel.svelte';

  type Note = {
    id: string;
    text: string;
    timestamp: string;
  };

  type CriticalPoint = {
    id: string;
    text: string;
    resolved: boolean;
  };

  type Task = {
    id: number;
    title: string;
    priority: string;
    completed: boolean;
    category?: string;
    files?: string[];
    deadline?: string;
    description?: string;
    notes?: string;
    progress?: number;
    critical_points?: string;
  };

  const API_URL = 'http://localhost:8000';
  
  let task = $state<Task | null>(null);
  let loading = $state(true);
  let taskId = $state<string>('');
  
  // Estados de edición
  let editingDescription = $state(false);
  let editingTitle = $state(false);
  let tempDescription = $state('');
  let tempTitle = $state('');
  
  // Notas
  let notes = $state<Note[]>([]);
  let newNoteText = $state('');
  let addingNote = $state(false);
  
  // Puntos críticos
  let criticalPoints = $state<CriticalPoint[]>([]);
  let newCriticalPoint = $state('');
  let addingCriticalPoint = $state(false);
  
  // Puntos críticos filtrados
  let pendingCriticalPoints = $derived(criticalPoints.filter(p => !p.resolved));
  let completedCriticalPoints = $derived(criticalPoints.filter(p => p.resolved));
  
  // Debug effect para ver cambios en puntos críticos
  $effect(() => {
    console.log('Estado de puntos críticos:');
    console.log('- Total:', criticalPoints.length);
    console.log('- Pendientes:', pendingCriticalPoints.length);
    console.log('- Completados:', completedCriticalPoints.length);
    console.log('- Lista completa:', criticalPoints);
  });
  
  // Modo read-only para tareas completadas
  let isTaskCompleted = $derived(task?.completed ?? false);
  
  // Progreso
  let editingProgress = $state(false);
  let tempProgress = $state(0);
  
  // Chat AI
  let chatOpen = $state(false);
  
  $effect(() => {
    const id = $page.params.id;
    if (id) {
      taskId = id;
      fetchTask();
    }
  });

  async function fetchTask() {
    try {
      const res = await fetch(`${API_URL}/tasks/${taskId}`);
      if (!res.ok) throw new Error('Tarea no encontrada');
      const data = await res.json();
      task = data;
      
      // Parsear notas
      if (data.notes) {
        try {
          notes = JSON.parse(data.notes);
        } catch {
          notes = [];
        }
      }
      
      // Parsear puntos críticos
      if (data.critical_points) {
        try {
          criticalPoints = JSON.parse(data.critical_points);
          console.log('Puntos críticos cargados:', criticalPoints);
        } catch {
          criticalPoints = [];
        }
      } else {
        criticalPoints = [];
      }
      
      loading = false;
    } catch (error) {
      console.error('Error fetching task:', error);
      loading = false;
    }
  }

  async function updateTask(updates: Partial<Task>) {
    if (!task) return;
    
    const formData = new FormData();
    formData.append('title', updates.title ?? task.title);
    formData.append('priority', updates.priority ?? task.priority);
    formData.append('completed', String(updates.completed ?? task.completed));
    formData.append('category', updates.category ?? task.category ?? 'General');
    
    if (task.deadline) formData.append('deadline', task.deadline);
    if (updates.description !== undefined) formData.append('description', updates.description);
    if (updates.notes !== undefined) formData.append('notes', updates.notes);
    if (updates.progress !== undefined) formData.append('progress', String(updates.progress));
    if (updates.critical_points !== undefined) formData.append('critical_points', updates.critical_points);
    
    try {
      const res = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'PUT',
        body: formData
      });
      
      if (res.ok) {
        await fetchTask();
      }
    } catch (error) {
      console.error('Error updating task:', error);
    }
  }

  function startEditDescription() {
    editingDescription = true;
    tempDescription = task?.description || '';
  }

  function cancelEditDescription() {
    editingDescription = false;
    tempDescription = '';
  }

  async function saveDescription() {
    await updateTask({ description: tempDescription });
    editingDescription = false;
  }

  function startEditTitle() {
    editingTitle = true;
    tempTitle = task?.title || '';
  }

  async function saveTitle() {
    await updateTask({ title: tempTitle });
    editingTitle = false;
  }

  function cancelEditTitle() {
    editingTitle = false;
    tempTitle = '';
  }

  function startEditProgress() {
    editingProgress = true;
    tempProgress = task?.progress || 0;
  }

  async function saveProgress() {
    await updateTask({ progress: tempProgress });
    editingProgress = false;
  }

  function cancelEditProgress() {
    editingProgress = false;
  }

  async function addNote() {
    if (!newNoteText.trim()) return;
    
    const newNote: Note = {
      id: Date.now().toString(),
      text: newNoteText,
      timestamp: new Date().toISOString()
    };
    
    notes = [...notes, newNote];
    await updateTask({ notes: JSON.stringify(notes) });
    newNoteText = '';
    addingNote = false;
  }

  async function deleteNote(noteId: string) {
    notes = notes.filter(n => n.id !== noteId);
    await updateTask({ notes: JSON.stringify(notes) });
  }

  async function addCriticalPoint() {
    if (!newCriticalPoint.trim()) return;
    
    const newPoint: CriticalPoint = {
      id: Date.now().toString(),
      text: newCriticalPoint,
      resolved: false
    };
    
    criticalPoints = [...criticalPoints, newPoint];
    console.log('Añadiendo punto crítico:', newPoint);
    console.log('Lista completa:', criticalPoints);
    await updateTask({ critical_points: JSON.stringify(criticalPoints) });
    newCriticalPoint = '';
    addingCriticalPoint = false;
  }

  async function toggleCriticalPoint(pointId: string) {
    console.log('Toggle punto crítico:', pointId);
    const before = [...criticalPoints];
    criticalPoints = criticalPoints.map(p => 
      p.id === pointId ? { ...p, resolved: !p.resolved } : p
    );
    console.log('Antes:', before);
    console.log('Después:', criticalPoints);
    await updateTask({ critical_points: JSON.stringify(criticalPoints) });
  }

  async function deleteCriticalPoint(pointId: string) {
    criticalPoints = criticalPoints.filter(p => p.id !== pointId);
    await updateTask({ critical_points: JSON.stringify(criticalPoints) });
  }

  function formatDate(dateString?: string) {
    if (!dateString) return 'Sin fecha límite';
    const [year, month, day] = dateString.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
  }

  function formatNoteDate(isoString: string) {
    const date = new Date(isoString);
    return date.toLocaleString('es-ES', { 
      day: 'numeric', 
      month: 'short', 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  }

  function getFileType(filename: string): 'image' | 'video' | 'file' {
    const ext = filename.split('.').pop()?.toLowerCase();
    if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(ext || '')) return 'image';
    if (['mp4', 'webm', 'ogg', 'mov'].includes(ext || '')) return 'video';
    return 'file';
  }

  function getPriorityColor(priority: string) {
    switch (priority) {
      case 'high': return '#ff7b54';
      case 'medium': return '#f6e05e';
      case 'low': return '#63b3ed';
      default: return '#7d8da6';
    }
  }

  function getPriorityLabel(priority: string) {
    switch (priority) {
      case 'high': return 'Alta';
      case 'medium': return 'Media';
      case 'low': return 'Baja';
      default: return priority;
    }
  }
</script>



<div class="task-detail-container"  role="application">
  
  <!-- BACKGROUND PARTICLES REMOVED -->
  
  <!-- MAIN CONTENT -->
  <div class="main-container">
    {#if loading}
      <div class="loading">
        <div class="spinner"></div>
        <p>Cargando tarea...</p>
      </div>
    {:else if !task}
      <div class="error">
        <p>No se encontró la tarea</p>
        <button onclick={() => goto('/tasklist')} class="back-btn-error">
          <ArrowLeft size={20} />
          Volver al listado
        </button>
      </div>
    {:else}
      <!-- Header -->
      <div class="header">
        <button onclick={() => goto('/tasklist')} class="back-btn">
          <ArrowLeft size={20} />
        </button>
        
        {#if isTaskCompleted}
          <div class="completed-banner">
            <CheckCircle2 size={20} />
            <span>Tarea Completada - Modo Solo Lectura</span>
            <button onclick={() => goto('/completed')} class="back-to-completed">
              Ver todas las completadas
            </button>
          </div>
        {/if}
        
        <div class="title-section">
          {#if editingTitle && !isTaskCompleted}
            <div class="edit-title-container">
              <input 
                type="text" 
                bind:value={tempTitle} 
                class="title-input"
              />
              <button onclick={saveTitle} class="save-btn" title="Guardar">
                <Save size={18} />
              </button>
              <button onclick={cancelEditTitle} class="cancel-btn" title="Cancelar">
                <X size={18} />
              </button>
            </div>
          {:else}
            <h1 class="task-title">
              {task.title}
              {#if !isTaskCompleted}
                <button onclick={startEditTitle} class="edit-icon-btn" title="Editar título">
                  <Pencil size={18} />
                </button>
              {/if}
            </h1>
          {/if}
          
          <div class="meta-info">
            <span class="badge priority" style="background: {getPriorityColor(task.priority)}">
              {getPriorityLabel(task.priority)}
            </span>
            <span class="badge category">{task.category || 'General'}</span>
            {#if task.deadline}
              <span class="badge deadline">
                <Calendar size={14} />
                {formatDate(task.deadline)}
              </span>
            {/if}
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="progress-section">
        <div class="progress-header">
          <span class="progress-label">
            <CheckCircle2 size={18} />
            Progreso
          </span>
          {#if editingProgress && !isTaskCompleted}
            <div class="progress-edit">
              <input 
                type="range" 
                min="0" 
                max="100" 
                bind:value={tempProgress}
                class="progress-slider"
              />
              <span class="progress-value">{tempProgress}%</span>
              <button onclick={saveProgress} class="save-btn-small">
                <Save size={14} />
              </button>
              <button onclick={cancelEditProgress} class="cancel-btn-small">
                <X size={14} />
              </button>
            </div>
          {:else}
            <div class="progress-display">
              <span class="progress-value">{task.progress || 0}%</span>
              {#if !isTaskCompleted}
                <button onclick={startEditProgress} class="edit-icon-btn-small">
                  <Pencil size={14} />
                </button>
              {/if}
            </div>
          {/if}
        </div>
        <div class="progress-bar">
          <div class="progress-fill" style="width: {task.progress || 0}%"></div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="content-grid">
        
        <!-- Description Section -->
        <section class="card description-card">
          <div class="card-header">
            <h2>
              <FileText size={20} />
              Descripción
            </h2>
            {#if !editingDescription && !isTaskCompleted}
              <button onclick={startEditDescription} class="edit-btn-header">
                <Pencil size={16} />
              </button>
            {/if}
          </div>
          
          {#if editingDescription && !isTaskCompleted}
            <div class="edit-area" transition:slide>
              <textarea 
                bind:value={tempDescription} 
                placeholder="Añade una descripción detallada..."
                class="textarea"
                rows="6"
              ></textarea>
              <div class="button-group">
                <button onclick={saveDescription} class="btn btn-primary">
                  <Save size={16} />
                  Guardar
                </button>
                <button onclick={cancelEditDescription} class="btn btn-secondary">
                  <X size={16} />
                  Cancelar
                </button>
              </div>
            </div>
          {:else}
            <div class="card-content">
              {#if task.description}
                <p class="description-text">{task.description}</p>
              {:else}
                <p class="empty-state">{isTaskCompleted ? 'Sin descripción.' : 'Sin descripción. Haz clic en editar para añadir una.'}</p>
              {/if}
            </div>
          {/if}
        </section>

        <!-- Files Section -->
        {#if task.files && task.files.length > 0}
          <section class="card files-card">
            <div class="card-header">
              <h2>
                <Paperclip size={20} />
                Archivos ({task.files.length})
              </h2>
            </div>
            <div class="card-content">
              <div class="files-grid">
                {#each task.files as file}
                  {@const fileType = getFileType(file)}
                  <a 
                    href={`${API_URL}/static/${file}`} 
                    target="_blank" 
                    rel="noopener"
                    class="file-item"
                  >
                    {#if fileType === 'image'}
                      <div class="file-preview image-preview">
                        <img src={`${API_URL}/static/${file}`} alt={file} />
                      </div>
                      <div class="file-info">
                        <ImageIcon size={16} />
                        <span class="file-name">{file}</span>
                      </div>
                    {:else if fileType === 'video'}
                      <div class="file-preview video-preview">
                        <Video size={32} />
                      </div>
                      <div class="file-info">
                        <Video size={16} />
                        <span class="file-name">{file}</span>
                      </div>
                    {:else}
                      <div class="file-preview file-icon-preview">
                        <FileIcon size={32} />
                      </div>
                      <div class="file-info">
                        <FileIcon size={16} />
                        <span class="file-name">{file}</span>
                      </div>
                    {/if}
                  </a>
                {/each}
              </div>
            </div>
          </section>
        {/if}

        <!-- Notes Section -->
        <section class="card notes-card">
          <div class="card-header">
            <h2>
              <FileText size={20} />
              Notas ({notes.length})
            </h2>
            {#if !addingNote && !isTaskCompleted}
              <button onclick={() => addingNote = true} class="add-btn">
                <Plus size={16} />
                Añadir
              </button>
            {/if}
          </div>
          
          <div class="card-content">
            {#if addingNote && !isTaskCompleted}
              <div class="add-note-form" transition:slide>
                <textarea 
                  bind:value={newNoteText}
                  placeholder="Escribe tu nota..."
                  class="textarea"
                  rows="3"
                ></textarea>
                <div class="button-group">
                  <button onclick={addNote} class="btn btn-primary">
                    <Plus size={16} />
                    Añadir
                  </button>
                  <button onclick={() => { addingNote = false; newNoteText = ''; }} class="btn btn-secondary">
                    <X size={16} />
                    Cancelar
                  </button>
                </div>
              </div>
            {/if}
            
            {#if notes.length === 0 && !addingNote}
              <p class="empty-state">{isTaskCompleted ? 'No hay notas.' : 'No hay notas todavía. Añade la primera!'}</p>
            {:else}
              <div class="notes-list">
                {#each notes as note (note.id)}
                  <div class="note-item" transition:slide>
                    <div class="note-content">
                      <p class="note-text">{note.text}</p>
                      <span class="note-date">{formatNoteDate(note.timestamp)}</span>
                    </div>
                    {#if !isTaskCompleted}
                      <button onclick={() => deleteNote(note.id)} class="delete-note-btn" title="Eliminar nota">
                        <Trash2 size={14} />
                      </button>
                    {/if}
                  </div>
                {/each}
              </div>
            {/if}
          </div>
        </section>

        <!-- Critical Points Section - Pending -->
        <section class="card critical-card">
          <div class="card-header">
            <h2>
              <AlertTriangle size={20} />
              Puntos Críticos Pendientes ({pendingCriticalPoints.length})
            </h2>
            {#if !addingCriticalPoint && !isTaskCompleted}
              <button onclick={() => addingCriticalPoint = true} class="add-btn">
                <Plus size={16} />
                Añadir
              </button>
            {/if}
          </div>
          
          <div class="card-content">
            {#if addingCriticalPoint && !isTaskCompleted}
              <div class="add-critical-form" transition:slide>
                <input 
                  type="text"
                  bind:value={newCriticalPoint}
                  placeholder="Describe el punto crítico..."
                  class="input"
                />
                <div class="button-group">
                  <button onclick={addCriticalPoint} class="btn btn-primary">
                    <Plus size={16} />
                    Añadir
                  </button>
                  <button onclick={() => { addingCriticalPoint = false; newCriticalPoint = ''; }} class="btn btn-secondary">
                    <X size={16} />
                    Cancelar
                  </button>
                </div>
              </div>
            {/if}
            
            {#if pendingCriticalPoints.length === 0 && !addingCriticalPoint}
              <p class="empty-state">{isTaskCompleted ? 'No hay puntos críticos pendientes.' : 'No hay puntos críticos pendientes. ¡Excelente trabajo!'}</p>
            {/if}
            
            {#if pendingCriticalPoints.length > 0}
              <div class="critical-list">
                {#each pendingCriticalPoints as point (point.id)}
                  <div class="critical-item" transition:slide>
                    <label class="checkbox-container">
                      <input 
                        type="checkbox" 
                        checked={false}
                        onchange={() => toggleCriticalPoint(point.id)}
                        disabled={isTaskCompleted}
                      />
                      <span class="checkmark"></span>
                    </label>
                    <span class="critical-text">{point.text}</span>
                    {#if !isTaskCompleted}
                      <button onclick={() => deleteCriticalPoint(point.id)} class="delete-critical-btn" title="Eliminar">
                        <Trash2 size={14} />
                      </button>
                    {/if}
                  </div>
                {/each}
              </div>
            {/if}
          </div>
        </section>

        <!-- Critical Points Section - Completed -->
        {#if completedCriticalPoints.length > 0}
          <section class="card critical-card completed-critical-card">
            <div class="card-header">
              <h2>
                <CheckCircle2 size={20} />
                Puntos Críticos Completados ({completedCriticalPoints.length})
              </h2>
            </div>
            
            <div class="card-content">
              <div class="critical-list">
                {#each completedCriticalPoints as point (point.id)}
                  <div class="critical-item resolved" transition:slide>
                    <label class="checkbox-container">
                      <input 
                        type="checkbox" 
                        checked={true}
                        onchange={() => toggleCriticalPoint(point.id)}
                        disabled={isTaskCompleted}
                      />
                      <span class="checkmark"></span>
                    </label>
                    <span class="critical-text">{point.text}</span>
                    {#if !isTaskCompleted}
                      <button onclick={() => deleteCriticalPoint(point.id)} class="delete-critical-btn" title="Eliminar">
                        <Trash2 size={14} />
                      </button>
                    {/if}
                  </div>
                {/each}
              </div>
            </div>
          </section>
        {/if}
      </div>
    {/if}
  </div>
  
  <!-- FLOATING AI BUTTON -->
  <button 
    class="floating-ai-btn" 
    onclick={() => chatOpen = true}
    aria-label="Abrir AI Assistant"
  >
    <Bot size={24} />
  </button>
  
  <!-- AI CHAT PANEL -->
  <ChatPanel bind:isOpen={chatOpen} taskId={task?.id} />
</div>

<style>
  /* --- LAYOUT & BASE --- */
  /* Removed unused .app styles */

  /* --- SIDEBAR --- */
  /* Removed unused sidebar styles */

  /* --- MAIN CONTAINER --- */
  .main-container {
  position: relative;
  width: 100%;
  height: auto;
  min-height: 100%;
  background: oklch(var(--background));
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
}

  @media (max-width: 768px) {
    .main-container {
      padding: 1rem;
      gap: 1rem;
    }
  }

  /* Loading & Error States */
  .loading,
  .error {
    background: oklch(var(--card));
    color: oklch(var(--card-foreground));
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 3rem;
    text-align: center;
    border: 2px solid oklch(var(--border));
    box-shadow: 
      0 20px 60px rgba(0, 0, 0, 0.5),
      0 10px 30px rgba(0, 0, 0, 0.3),
      0 0 0 1px oklch(var(--border));
  }



  .spinner {
    width: 48px;
    height: 48px;
    border: 4px solid rgba(124, 58, 237, 0.2);
    border-top-color: #7c3aed;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .back-btn-error {
    margin-top: 1.5rem;
    padding: 0.75rem 1.5rem;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    color: white;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.95rem;
    font-weight: 600;
    transition: all 0.2s ease;
  }

  .back-btn-error:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  }

  /* Header */
  .header {
    background: color-mix(in oklch, oklch(var(--card)), black 5%);
    color: oklch(var(--card-foreground));
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 2px solid oklch(var(--border));
    box-shadow: 
      0 8px 25px rgba(0, 0, 0, 0.4),
      0 3px 10px rgba(0, 0, 0, 0.25),
      inset 0 1px 0 rgba(255, 255, 255, 0.08);
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: flex-start;
  }



  .completed-banner {
    width: 100%;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
  }

  .completed-banner span {
    flex: 1;
  }

  .back-to-completed {
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: 2px solid white;
    background: transparent;
    color: white;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.875rem;
    transition: all 0.2s ease;
  }

  .back-to-completed:hover {
    background: white;
    color: #10b981;
    transform: translateY(-2px);
  }

  .back-btn {
    padding: 0.75rem;
    border-radius: 12px;
    border: none;
    background: rgba(124, 58, 237, 0.1);
    color: #7c3aed;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .back-btn:hover {
    background: rgba(124, 58, 237, 0.2);
    transform: translateX(-4px);
  }



  .title-section {
    flex: 1;
  }

  .task-title {
    font-weight: 700;
    color: oklch(var(--card-foreground));
    margin: 0 0 0.75rem 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }



  .edit-title-container {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-bottom: 0.75rem;
  }

  .title-input {
    flex: 1;
    padding: 0.75rem 1rem;
    border: 2px solid oklch(var(--primary) / 30%);
    border-radius: 12px;
    font-size: 1.5rem;
    font-weight: 700;
    background: oklch(var(--card));
    color: oklch(var(--card-foreground));
  }



  .edit-icon-btn,
  .edit-icon-btn-small {
    padding: 0.5rem;
    border-radius: 8px;
    border: none;
    background: rgba(124, 58, 237, 0.1);
    color: #7c3aed;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .edit-icon-btn-small {
    padding: 0.375rem;
  }

  .edit-icon-btn:hover,
  .edit-icon-btn-small:hover {
    background: rgba(124, 58, 237, 0.2);
    transform: scale(1.05);
  }



  .save-btn,
  .cancel-btn {
    padding: 0.75rem;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: all 0.2s ease;
  }

  .save-btn {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
  }

  .cancel-btn {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }

  .save-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  }

  .cancel-btn:hover {
    background: rgba(239, 68, 68, 0.2);
  }

  .meta-info {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.375rem 0.75rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 600;
  }

  .badge.priority {
    color: white;
  }

  .badge.category {
    background: rgba(59, 130, 246, 0.1);
    color: #3b82f6;
  }

  .badge.deadline {
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
  }



  /* Progress Section */
  .progress-section {
    background: color-mix(in oklch, oklch(var(--card)), black 5%);
    color: oklch(var(--card-foreground));
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 2px solid oklch(var(--border));
    box-shadow: 
      0 8px 25px rgba(0, 0, 0, 0.4),
      0 3px 10px rgba(0, 0, 0, 0.25),
      inset 0 1px 0 rgba(255, 255, 255, 0.08);
  }



  .progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .progress-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    color: oklch(var(--card-foreground));
  }



  .progress-display,
  .progress-edit {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .progress-value {
    font-size: 1.125rem;
    font-weight: 700;
    color: oklch(var(--primary));
  }



  .progress-slider {
    width: 150px;
  }

  .save-btn-small,
  .cancel-btn-small {
    padding: 0.375rem;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: all 0.2s ease;
  }

  .save-btn-small {
    background: #10b981;
    color: white;
  }

  .cancel-btn-small {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }

  .progress-bar {
    height: 14px;
    background: oklch(var(--muted));
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid oklch(var(--border));
    box-shadow: inset 0 2px 4px oklch(0 0 0 / 10%);
  }



  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, oklch(var(--primary)), oklch(var(--primary) / 80%));
    border-radius: 10px;
    transition: width 0.5s ease;
    box-shadow: 0 2px 8px oklch(var(--primary) / 40%);
    position: relative;
  }

  .progress-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(180deg, oklch(1 0 0 / 20%), transparent);
    border-radius: 10px 10px 0 0;
  }

  /* Content Grid */
  .content-grid {
    display: grid;
    gap: 1.5rem;
    grid-template-columns: 1fr;
  }

  @media (min-width: 768px) {
    .content-grid {
      grid-template-columns: repeat(2, 1fr);
    }
    
    .description-card {
      grid-column: 1 / -1;
    }
  }

  /* Cards */
  .card {
    background: color-mix(in oklch, oklch(var(--card)), black 5%);
    color: oklch(var(--card-foreground));
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 1.5rem;
    border: 2px solid oklch(var(--border));
    box-shadow: 
      0 8px 25px rgba(0, 0, 0, 0.4),
      0 3px 10px rgba(0, 0, 0, 0.25),
      inset 0 1px 0 rgba(255, 255, 255, 0.08);
    transition: all 0.3s ease;
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: 
      0 12px 30px rgba(0, 0, 0, 0.45),
      0 5px 12px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    border-color: oklch(var(--primary) / 50%);
  }



  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .card-header h2 {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.25rem;
    font-weight: 600;
    color: oklch(var(--card-foreground));
    margin: 0;
  }



  .edit-btn-header,
  .add-btn {
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    border: none;
    background: rgba(124, 58, 237, 0.1);
    color: #7c3aed;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.375rem;
    transition: all 0.2s ease;
  }

  .edit-btn-header:hover,
  .add-btn:hover {
    background: rgba(124, 58, 237, 0.2);
    transform: translateY(-2px);
  }



  .card-content {
    color: oklch(var(--muted-foreground));
  }



  .empty-state {
    padding: 2rem;
    color: #94a3b8;
    font-style: italic;
  }

  .description-text {
    line-height: 1.6;
    white-space: pre-wrap;
  }

  /* Textarea & Input */
  .textarea,
  .input {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid oklch(var(--border));
    border-radius: 12px;
    font-family: inherit;
    font-size: 0.95rem;
    background: oklch(var(--input));
    color: oklch(var(--card-foreground));
    resize: vertical;
    transition: all 0.2s ease;
  }

  .textarea:focus,
  .input:focus {
    outline: none;
    border-color: oklch(var(--primary));
    box-shadow: 0 0 0 3px oklch(var(--primary) / 10%);
  }



  /* Button Groups */


  .btn {
    padding: 0.625rem 1rem;
    border-radius: 10px;
    border: none;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.375rem;
    transition: all 0.2s ease;
  }

  .btn-primary {
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    color: white;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  }

  .btn-secondary {
    background: oklch(var(--secondary));
    color: oklch(var(--secondary-foreground));
  }

  .btn-secondary:hover {
    background: oklch(var(--secondary) / 80%);
  }



  /* Files Grid */
  .files-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }

  .file-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    text-decoration: none;
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.2s ease;
    border: 2px solid transparent;
  }

  .file-item:hover {
    transform: translateY(-4px);
    border-color: oklch(var(--primary) / 30%);
  }

  .file-item:hover .file-preview {
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }

  .file-preview {
    aspect-ratio: 1;
    border-radius: 12px;
    overflow: hidden;
    background: oklch(var(--muted));
    border: 1px solid oklch(var(--border));
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }



  .image-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .video-preview,
  .file-icon-preview {
    color: #7c3aed;
  }



  .file-info {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    color: oklch(var(--muted-foreground));
    font-size: 0.875rem;
  }



  .file-name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* Notes List */
  .notes-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: 400px;
    overflow-y: auto;
    padding-right: 0.5rem;
  }

  .notes-list::-webkit-scrollbar {
    width: 8px;
  }

  .notes-list::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.05);
    border-radius: 10px;
  }



  .notes-list::-webkit-scrollbar-thumb {
    background: rgba(124, 58, 237, 0.3);
    border-radius: 10px;
  }

  .notes-list::-webkit-scrollbar-thumb:hover {
    background: rgba(124, 58, 237, 0.5);
  }

  .note-item {
    display: flex;
    gap: 0.75rem;
    padding: 1rem;
    background: oklch(var(--muted));
    border-radius: 12px;
    border: 1px solid oklch(var(--border));
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
  }

  .note-item:hover {
    border-color: oklch(var(--primary) / 30%);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    transform: translateX(2px);
  }



  .note-content {
    flex: 1;
  }

  .note-text {
    margin: 0 0 0.375rem 0;
    line-height: 1.5;
    color: oklch(var(--card-foreground));
  }



  .note-date {
    font-size: 0.75rem;
    color: #94a3b8;
  }

  .delete-note-btn,
  .delete-critical-btn {
    padding: 0.375rem;
    border-radius: 6px;
    border: none;
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .delete-note-btn:hover,
  .delete-critical-btn:hover {
    background: rgba(239, 68, 68, 0.2);
    transform: scale(1.05);
  }

  /* Critical Points List */
  .critical-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: 400px;
    overflow-y: auto;
    padding-right: 0.5rem;
  }

  .critical-list::-webkit-scrollbar {
    width: 8px;
  }

  .critical-list::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.05);
    border-radius: 10px;
  }



  .critical-list::-webkit-scrollbar-thumb {
    background: rgba(239, 68, 68, 0.3);
    border-radius: 10px;
  }

  .critical-list::-webkit-scrollbar-thumb:hover {
    background: rgba(239, 68, 68, 0.5);
  }

  .critical-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: rgba(239, 68, 68, 0.08);
    border-radius: 12px;
    border: 1px solid rgba(239, 68, 68, 0.25);
    box-shadow: 0 1px 3px rgba(239, 68, 68, 0.15);
    transition: all 0.2s ease;
  }

  .critical-item:hover {
    border-color: rgba(239, 68, 68, 0.4);
    box-shadow: 0 2px 6px rgba(239, 68, 68, 0.25);
    transform: translateX(2px);
  }

  .critical-item.resolved {
    background: rgba(16, 185, 129, 0.08);
    border-color: rgba(16, 185, 129, 0.25);
    box-shadow: 0 1px 3px rgba(16, 185, 129, 0.15);
    opacity: 0.85;
  }

  .completed-critical-card {
    border-left: 4px solid #10b981;
    background: linear-gradient(135deg, oklch(var(--card)), oklch(var(--card) / 95%));
    box-shadow: 
      0 10px 40px rgba(0, 0, 0, 0.5),
      0 4px 12px rgba(16, 185, 129, 0.2),
      -4px 0 0 0 #10b981,
      0 0 0 1px oklch(var(--border));
  }

  .completed-critical-card .card-header h2 {
    color: #10b981;
  }



  .completed-critical-card .critical-item {
    background: rgba(16, 185, 129, 0.1);
    border-color: rgba(16, 185, 129, 0.3);
    box-shadow: 0 1px 3px rgba(16, 185, 129, 0.2);
    opacity: 1;
  }

  .critical-text {
    flex: 1;
    color: oklch(var(--card-foreground));
  }

  .critical-item.resolved .critical-text {
    text-decoration: line-through;
    color: oklch(var(--muted-foreground));
  }





  /* Checkbox */
  .checkbox-container {
 cursor: pointer;
    user-select: none;
  }

  .checkbox-container input:disabled {
    cursor: not-allowed;
  }

  .checkbox-container:has(input:disabled) {
    cursor: not-allowed;
    opacity: 0.6;
  }

  .checkbox-container input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }

  .checkmark {
    display: block;
    height: 20px;
    width: 20px;
    background-color: oklch(var(--muted));
    border-radius: 6px;
    border: 2px solid oklch(var(--border));
    transition: all 0.2s ease;
  }



  .checkbox-container input:checked ~ .checkmark {
    background-color: #10b981;
    border-color: #10b981;
  }

  .checkmark:after {
    content: "";
    position: absolute;
    display: none;
    left: 6px;
    top: 2px;
    width: 4px;
    height: 9px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
  }

  .checkbox-container input:checked ~ .checkmark:after {
    display: block;
  }

  @media (max-width: 768px) {
    .header,
    .progress-section,
    .card {
      padding: 1rem;
    }
    
    .task-title {
      font-size: 1.5rem;
    }
    
    .files-grid {
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    }
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
    box-shadow: 0 12px 40px rgba(255, 123, 84, 0.5);
    z-index: 1000;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .floating-ai-btn:hover {
    transform: scale(1.15) rotate(10deg);
    box-shadow: 0 16px 50px rgba(255, 123, 84, 0.7);
  }

  .floating-ai-btn:active {
    transform: scale(1.05);
  }

  @media (max-width: 768px) {
    .floating-ai-btn {
      bottom: 1.5rem;
      right: 1.5rem;
      width: 56px;
      height: 56px;
    }
  }
</style>

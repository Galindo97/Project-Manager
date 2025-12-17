<script lang="ts">
  import { onMount } from 'svelte';
  import { slide, fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import * as AlertDialog from '$lib/components/ui/alert-dialog';
  import * as Dialog from '$lib/components/ui/dialog';
  import { Input } from '$lib/components/ui/input';
  import { Pencil, Trash2, Paperclip, Clock, CheckCircle2, Flame, BarChart3, Clipboard, Sun, Moon, XCircle, Trash, Calendar, Menu, X, Home, ListTodo, Award, Settings, User, Search, LogOut, Bot } from 'lucide-svelte';
  import { authStore } from '$stores/auth';
  import { tasksAPI } from '$lib/api';
  import TaskList from '$lib/TaskList.svelte';
  import ChatPanel from '$lib/ChatPanel.svelte';

  // --- LÓGICA DE TAREAS ---
  type Task = {
    id: number;
    title: string;
    priority: string;
    completed: boolean;
    category?: string;
    files?: string[];
    deadline?: string;
    due_date?: string;
    description?: string;
  };
  let tasks = $state<Task[]>([]);

  let newTaskTitle = $state('');
  let newTaskPriority = $state('');
  let newTaskDeadline = $state('');
  let newTaskFiles = $state<FileList | null>(null);
  let fileInputRef: HTMLInputElement;
  let deadlineInputRef: HTMLInputElement;
  let taskToDelete = $state<number | null>(null);
  let showDeleteDialog = $state(false);
  let showDeleteMultipleDialog = $state(false);

  // Estado para edición
  let showEditDialog = $state(false);
  let taskToEdit = $state<Task | null>(null);
  let editTitle = $state('');
  let editPriority = $state('');
  let editCategory = $state('');
  let editDeadline = $state('');

  // Estado para filtros
  let filterPriority = $state<'all' | 'high' | 'medium' | 'low' | 'overdue'>('all');
  let showFilterDropdown = $state(false);
  let searchQuery = $state('');
  
  // Estado para selección múltiple
  let selectedTasks = $state<Set<number>>(new Set());

  // Estadísticas reactivas
  let completedCount = $derived(tasks.filter(t => t.completed).length);
  let pendingCount = $derived(tasks.filter(t => !t.completed).length);
  let highPriorityCount = $derived(tasks.filter(t => getPriorityClass(t) === 'high' && !t.completed).length);
  let completionRate = $derived(tasks.length > 0 ? Math.round((completedCount / tasks.length) * 100) : 0);

  // Tareas filtradas (excluir completadas) - usa prioridad dinámica según deadline
  let filteredTasks = $derived(
    tasks.filter(t => {
      const notCompleted = !t.completed;
      
      // Filtro de búsqueda
      const matchesSearch = searchQuery === '' || 
        t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (t.category && t.category.toLowerCase().includes(searchQuery.toLowerCase()));
      
      // Filtro especial para vencidas
      if (filterPriority === 'overdue') {
        const daysUntil = getDaysUntilDeadline(t.deadline);
        return notCompleted && daysUntil < 0 && matchesSearch;
      }
      
      // Filtros normales de prioridad
      const dynamicPriority = getPriorityClass(t);
      const matchesFilter = filterPriority === 'all' || dynamicPriority === filterPriority;
      return matchesFilter && notCompleted && matchesSearch;
    })
  );


  async function toggleTask(id: number) {
    // Alternar selección de la tarea
    if (selectedTasks.has(id)) {
      selectedTasks.delete(id);
      selectedTasks = new Set(selectedTasks); // Crear nuevo Set para reactividad
    } else {
      selectedTasks.add(id);
      selectedTasks = new Set(selectedTasks); // Crear nuevo Set para reactividad
    }
  }

  function toggleSelectAll() {
    // Si todas las tareas filtradas están seleccionadas, deseleccionar todas
    const allSelected = filteredTasks.every(t => selectedTasks.has(t.id));
    
    if (allSelected) {
      selectedTasks = new Set();
    } else {
      // Seleccionar todas las tareas filtradas
      selectedTasks = new Set(filteredTasks.map(t => t.id));
    }
  }

  // Verificar si todas las tareas filtradas están seleccionadas
  let allTasksSelected = $derived(
    filteredTasks.length > 0 && filteredTasks.every(t => selectedTasks.has(t.id))
  );

  async function completeSelectedTasks() {
    // Marcar todas las tareas seleccionadas como completadas en el backend
    for (const id of selectedTasks) {
      try {
        await tasksAPI.update(id, { completed: true });
      } catch (error) {
        console.error('Error completing task:', error);
      }
    }
    
    // Limpiar selección y recargar tareas
    selectedTasks = new Set();
    await fetchTasks();
  }
  
  async function deleteSelectedTasks() {
    // Eliminar las tareas seleccionadas
    for (const id of selectedTasks) {
      try {
        await tasksAPI.delete(id);
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
    
    // Limpiar selección y recargar tareas
    selectedTasks = new Set();
    showDeleteMultipleDialog = false;
    await fetchTasks();
  }
  
  function openDeleteMultipleDialog() {
    showDeleteMultipleDialog = true;
  }
  
  function cancelSelection() {
    selectedTasks = new Set();
  }

  // Helper para calcular días hasta deadline (para ordenamiento)
  function getDaysUntilDeadline(deadline?: string): number {
    if (!deadline) return Infinity; // Sin deadline va al final
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const [year, month, day] = deadline.split('-').map(Number);
    const deadlineDate = new Date(year, month - 1, day);
    deadlineDate.setHours(0, 0, 0, 0);
    
    const diffTime = deadlineDate.getTime() - today.getTime();
    return Math.round(diffTime / (1000 * 60 * 60 * 24));
  }

  // Helper para formatear y verificar fechas
  function getDeadlineStatus(deadline?: string) {
    if (!deadline) return null;
    
    const diffDays = getDaysUntilDeadline(deadline);
    
    if (diffDays < 0) return { text: 'Vencida', class: 'overdue' };
    if (diffDays === 0) return { text: 'Hoy', class: 'today' };
    if (diffDays === 1) return { text: 'Mañana', class: 'tomorrow' };
    if (diffDays <= 3) return { text: `${diffDays} días`, class: 'soon' };
    
    // Formato de fecha normal
    const [year, month, day] = deadline.split('-').map(Number);
    const deadlineDate = new Date(year, month - 1, day);
    const options: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'short' };
    return { text: deadlineDate.toLocaleDateString('es-ES', options), class: 'normal' };
  }

  // Helper para obtener color de prioridad dinámico según deadline
  function getPriorityClass(task: Task): string {
    const daysUntil = getDaysUntilDeadline(task.deadline);
    
    // Si está vencida o vence hoy/mañana, siempre es crítica
    if (daysUntil <= 1) return 'high';
    
    // Si vence en 2-3 días, es media-alta
    if (daysUntil <= 3) return task.priority === 'low' ? 'medium' : task.priority;
    
    // Si vence en 4-7 días y es high, se mantiene high
    if (daysUntil <= 7 && task.priority === 'high') return 'high';
    
    // Resto mantiene su prioridad original
    return task.priority;
  }

  async function deleteTask() {
    if (taskToDelete === null) return;
    try {
      await tasksAPI.delete(taskToDelete);
      taskToDelete = null;
      await fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  }

  function openDeleteDialog(id: number) {
    taskToDelete = id;
    showDeleteDialog = true;
  }

  async function toggleCompleteTask(id: number) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    
    try {
      await tasksAPI.update(id, { completed: !task.completed });
      await fetchTasks();
    } catch (error) {
      console.error('Error toggling task:', error);
    }
  }

  function openEditDialog(task: Task) {
    taskToEdit = task;
    editTitle = task.title;
    editPriority = task.priority;
    editCategory = task.category || 'General';
    editDeadline = task.deadline || '';
    showEditDialog = true;
  }

  async function saveEditTask() {
    if (!taskToEdit || !editTitle.trim()) return;
    
    try {
      await tasksAPI.update(taskToEdit.id, {
        title: editTitle,
        priority: editPriority,
        category: editCategory || 'General',
        due_date: editDeadline || undefined
      });
      
      showEditDialog = false;
      taskToEdit = null;
      await fetchTasks();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  }


  async function addTask() {
    if (!newTaskTitle.trim() || !newTaskPriority) return;
    
    try {
      await tasksAPI.create({
        title: newTaskTitle,
        priority: newTaskPriority,
        category: 'General',
        due_date: newTaskDeadline || undefined
      });
      
      newTaskTitle = '';
      newTaskPriority = '';
      newTaskDeadline = '';
      newTaskFiles = null;
      await fetchTasks();
    } catch (error) {
      console.error('Error creating task:', error);
    }
  }

  async function fetchTasks() {
    try {
      const fetchedTasks = await tasksAPI.getAll();
      
      // Convertir due_date a deadline para compatibilidad
      const formattedTasks = fetchedTasks.map((task: any) => ({
        ...task,
        deadline: task.due_date ? task.due_date.split('T')[0] : undefined
      }));
      
      // Ordenar por deadline primero (más urgente primero), luego por prioridad
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      tasks = formattedTasks.sort((a: Task, b: Task) => {
        const daysA = getDaysUntilDeadline(a.deadline);
        const daysB = getDaysUntilDeadline(b.deadline);
        
        // Primero ordenar por días hasta deadline (menos días = más urgente)
        if (daysA !== daysB) {
          return daysA - daysB;
        }
      
        // Si tienen el mismo deadline (o ambos sin deadline), ordenar por prioridad
        return priorityOrder[a.priority as keyof typeof priorityOrder] - priorityOrder[b.priority as keyof typeof priorityOrder];
      });
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  }

  // Cerrar dropdown al hacer clic fuera
  function handleClickOutside(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (showFilterDropdown && !target.closest('.filter-section')) {
      showFilterDropdown = false;
    }
  }

  // --- LÓGICA DE FONDO (PARTÍCULAS) ---
  // (Reutilizamos la lógica optimizada del login para mantener consistencia visual)
  let darkMode = $state(false);
  
  let chatOpen = $state(false);
  
  // Cargar preferencia guardada al inicio
  if (typeof window !== 'undefined') {
    const savedMode = localStorage.getItem('darkMode');
    darkMode = savedMode === 'true';
  }

  
  
  const SHAPE_COUNT = 40;
  const FIXED_SIZE = 40;
  const colorsDark = ['#7c3aed', '#2563eb', '#db2777', '#06b6d4'];
  const colorsLight = ['#a78bfa', '#60a5fa', '#f472b6', '#22d3ee'];
  
  let shapesData = $state<any[]>([]);
  let shapeElements: (HTMLDivElement | null)[] = [];
  let containerWidth: number;
  let containerHeight: number;
  let mouseX = -1000, mouseY = -1000;

  onMount(() => {
    // Verificar autenticación y cargar datos
    (async () => {
      try {
        await authStore.loadUser();
        await fetchTasks();
      } catch (error) {
        window.location.href = '/login';
        return;
      }
    })();
    
    updateDimensions();
    window.addEventListener('resize', updateDimensions);

    shapesData = Array.from({ length: SHAPE_COUNT }).map(() => ({
      x: Math.random() * containerWidth,
      y: Math.random() * containerHeight,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      rotation: Math.random() * 360,
      rotSpeed: (Math.random() - 0.5) * 0.5,
      type: Math.floor(Math.random() * 3),
      colorIndex: Math.floor(Math.random() * colorsDark.length)
    }));

    let frame: number;
    const loop = () => {
      animateShapes();
      frame = requestAnimationFrame(loop);
    };
    loop();

    return () => {
      window.removeEventListener('resize', updateDimensions);
      cancelAnimationFrame(frame);
    };
  });

  function updateDimensions() {
    if (typeof window !== 'undefined') {
      containerWidth = window.innerWidth;
      containerHeight = window.innerHeight;
    }
  }

  function animateShapes() {
    shapesData.forEach((s, i) => {
      const el = shapeElements[i];
      if (!el) return;

      s.x += s.vx;
      s.y += s.vy;
      s.rotation += s.rotSpeed;

      // Rebote infinito
      if (s.x < -50) s.x = containerWidth + 50;
      if (s.x > containerWidth + 50) s.x = -50;
      if (s.y < -50) s.y = containerHeight + 50;
      if (s.y > containerHeight + 50) s.y = -50;

      // Interacción mouse
      const dx = s.x - mouseX;
      const dy = s.y - mouseY;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 200) {
        const force = (200 - dist) / 200;
        s.x += Math.cos(Math.atan2(dy, dx)) * force * 3;
        s.y += Math.sin(Math.atan2(dy, dx)) * force * 3;
      }

      el.style.transform = `translate(${s.x}px, ${s.y}px) rotate(${s.rotation}deg)`;
    });
  }
</script>



<div class="tasklist-container" role="application" onmousemove={(e) => { mouseX = e.clientX; mouseY = e.clientY; }}>
  
  <!-- Contenedor principal centrado -->
  <div class="main-content">
    <!-- Hero Section -->
    <div class="page-hero">
      <div class="hero-badge">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 11l3 3L22 4"/>
          <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
        </svg>
        <span>Gestión de Tareas</span>
      </div>
      <h1 class="hero-title">
        <span class="title-gradient">Mis Tareas</span>
        <span class="title-accent">organiza tu día</span>
      </h1>
      <p class="hero-description">
        Mantén el control de tus proyectos y aumenta tu productividad con una gestión eficiente de tareas.
      </p>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card" class:active={pendingCount > 0}>
        <div class="icon-bg blue"><ListTodo size={20} strokeWidth={2.5} /></div>
        <div class="stat-data">
          <span class="value">{pendingCount}</span>
          <span class="label">Pendientes</span>
        </div>
      </div>
      
      <div class="stat-card" class:active={completedCount > 0}>
        <a href="/completed" class="stat-link">
          <div class="icon-bg green"><CheckCircle2 size={20} strokeWidth={2.5} /></div>
          <div class="stat-data">
            <span class="value">{completedCount}</span>
            <span class="label">Completadas</span>
          </div>
        </a>
      </div>
      
      <div class="stat-card" class:active={highPriorityCount > 0}>
        <div class="icon-bg red"><Flame size={20} strokeWidth={2.5} /></div>
        <div class="stat-data">
          <span class="value">{highPriorityCount}</span>
          <span class="label">Prioridad Alta</span>
        </div>
      </div>
      
      <div class="stat-card progress-card">
        <div class="icon-bg purple"><BarChart3 size={20} strokeWidth={2.5} /></div>
        <div class="stat-data full-width">
          <div class="flex-between">
            <span class="label">Progreso Total</span>
            <span class="value-small">{completionRate}%</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" style="width: {completionRate}%"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Task Section -->
    <form class="add-task-form" onsubmit={(e) => { e.preventDefault(); addTask(); }}>
      <div class="task-input-row">
        <input 
          type="text" 
          placeholder="¡Añade tu tarea o proyecto!" 
          bind:value={newTaskTitle}
        />
        <select bind:value={newTaskPriority}>
          <option value="" disabled selected>Selecciona prioridad</option>
          <option value="low">Baja</option>
          <option value="medium">Media</option>
          <option value="high">Alta</option>
        </select>
        <!-- Campo de fecha límite (opcional) -->
        <input 
          type="date" 
          class="deadline-input-visible"
          bind:this={deadlineInputRef}
          bind:value={newTaskDeadline}
          placeholder="Fecha límite"
          title="Fecha límite (opcional)"
        />
        <!-- Icono para adjuntar archivos -->
        <button type="button" class="attach-btn" onclick={() => fileInputRef.click()} title="Adjuntar archivos" aria-label="Adjuntar archivos">
          <Paperclip size={16} strokeWidth={2} />
        </button>
        <button type="submit" disabled={!newTaskTitle || !newTaskPriority} class="submit-btn">
          +
        </button>
      </div>
      <input type="file" multiple accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt" bind:this={fileInputRef} style="display:none" onchange={(e) => newTaskFiles = (e.target as HTMLInputElement)?.files} />
      {#if newTaskFiles && newTaskFiles.length > 0}
        <div class="files-wrapper-with-btn">
          <button type="button" class="clear-files-btn" onclick={() => { newTaskFiles = null; if (fileInputRef) fileInputRef.value = ''; }} title="Eliminar archivos">
            ✕
          </button>
          <div class="files-compact-preview">
            {#each Array.from(newTaskFiles) as file, index}
              <div class="file-mini-item">
                {#if file.type.startsWith('image/')}
                  <img src={URL.createObjectURL(file)} alt={file.name} class="mini-preview-img" />
                {:else}
                  <div class="mini-file-icon">
                    {#if file.type.includes('pdf')}
                      📄
                    {:else if file.type.includes('word') || file.name.endsWith('.doc') || file.name.endsWith('.docx')}
                      📝
                    {:else if file.type.includes('sheet') || file.name.endsWith('.xls') || file.name.endsWith('.xlsx')}
                      📊
                    {:else if file.type.includes('presentation') || file.name.endsWith('.ppt') || file.name.endsWith('.pptx')}
                      📽️
                    {:else}
                      📎
                    {/if}
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        </div>
      {/if}
    </form>

    <!-- Filter Section -->
    <div class="filter-section-wrapper">
      <!-- Botones de acción (solo visibles cuando hay tareas seleccionadas) -->
      {#if selectedTasks.size > 0}
        <div class="action-buttons" transition:slide|local={{ duration: 200, axis: 'x' }}>
          <button 
            class="complete-selected-btn" 
            onclick={completeSelectedTasks}
            type="button"
            title="Completar tareas seleccionadas"
          >
            <CheckCircle2 size={18} strokeWidth={2.5} />
          </button>
          <button 
            class="delete-selected-btn" 
            onclick={openDeleteMultipleDialog}
            type="button"
            title="Eliminar tareas seleccionadas"
          >
            <Trash size={16} strokeWidth={2.5} />
          </button>
        </div>
      {/if}
      
      <div class="filter-section">
        <!-- Botón Seleccionar Todas -->
        <button 
          class="select-all-btn" 
          class:all-selected={allTasksSelected}
          onclick={toggleSelectAll}
          type="button"
          title={allTasksSelected ? "Deseleccionar todas" : "Seleccionar todas"}
          disabled={filteredTasks.length === 0}
        >
          {#if allTasksSelected}
            <span>Deseleccionar</span>
          {:else}
            <span>Seleccionar todas</span>
          {/if}
        </button>
        <button 
          class="filter-trigger" 
          onclick={() => showFilterDropdown = !showFilterDropdown}
          type="button"
        >
          <span class="filter-text">
            Filtrar
            {#if filterPriority !== 'all'}
              <span class="filter-badge">
                {filterPriority === 'high' ? 'Alta' : filterPriority === 'medium' ? 'Media' : filterPriority === 'low' ? 'Baja' : 'Vencidas'}
              </span>
            {/if}
          </span>
          <svg 
            class="chevron" 
            class:open={showFilterDropdown}
            width="16" 
            height="16" 
            viewBox="0 0 16 16" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <polyline points="4 6 8 10 12 6"></polyline>
          </svg>
        </button>
        
        {#if showFilterDropdown}
          <div class="filter-dropdown" transition:slide|local={{ duration: 200 }}>
            <button 
              class="dropdown-item" 
              class:active={filterPriority === 'all'}
              onclick={() => { filterPriority = 'all'; showFilterDropdown = false; }}
            >
              Todas las tareas
            </button>
            <button 
              class="dropdown-item priority-overdue" 
              class:active={filterPriority === 'overdue'}
              onclick={() => { filterPriority = 'overdue'; showFilterDropdown = false; }}
            >
              <span class="priority-dot overdue"></span>
              Tareas Vencidas
            </button>
            <button 
              class="dropdown-item priority-high" 
              class:active={filterPriority === 'high'}
              onclick={() => { filterPriority = 'high'; showFilterDropdown = false; }}
            >
              <span class="priority-dot high"></span>
              Prioridad Alta
            </button>
            <button 
              class="dropdown-item priority-medium" 
              class:active={filterPriority === 'medium'}
              onclick={() => { filterPriority = 'medium'; showFilterDropdown = false; }}
            >
              <span class="priority-dot medium"></span>
              Prioridad Media
            </button>
            <button 
              class="dropdown-item priority-low" 
              class:active={filterPriority === 'low'}
              onclick={() => { filterPriority = 'low'; showFilterDropdown = false; }}
            >
              <span class="priority-dot low"></span>
              Prioridad Baja
            </button>
          </div>
        {/if}
      </div>
    </div>

    <!-- Search Bar -->
    <div class="search-container">
      <div class="search-wrapper">
        <Search size={18} class="search-icon" />
        <input 
          type="text" 
          class="search-input"
          placeholder="Buscar tareas por título o categoría..."
          bind:value={searchQuery}
        />
        {#if searchQuery}
          <button class="clear-search" onclick={() => searchQuery = ''} aria-label="Limpiar búsqueda">
            <XCircle size={16} />
          </button>
        {/if}
      </div>
    </div>
    
    
    <!-- Task List -->
    <div class="task-list-container">
      <TaskList 
        tasks={filteredTasks} 
        onSelect={(id) => window.location.href = `/task/${id}`}
        onToggleComplete={toggleCompleteTask}
        onDelete={(id) => openDeleteDialog(id)}
        onEdit={(task) => openEditDialog(task)}
      />
    </div>
  </div>

  <!-- Alert Dialog para confirmar eliminación -->
  <AlertDialog.Root bind:open={showDeleteDialog}>
    <AlertDialog.Content>
      <AlertDialog.Header>
        <AlertDialog.Title>¿Estás seguro?</AlertDialog.Title>
        <AlertDialog.Description>
          Esta acción eliminará permanentemente la tarea. No se puede deshacer.
        </AlertDialog.Description>
      </AlertDialog.Header>
      <AlertDialog.Footer>
        <AlertDialog.Cancel>Cancelar</AlertDialog.Cancel>
        <AlertDialog.Action onclick={() => { deleteTask(); showDeleteDialog = false; }}>Eliminar</AlertDialog.Action>
      </AlertDialog.Footer>
    </AlertDialog.Content>
  </AlertDialog.Root>

  <!-- Alert Dialog para confirmar eliminación múltiple -->
  <AlertDialog.Root bind:open={showDeleteMultipleDialog}>
    <AlertDialog.Content>
      <AlertDialog.Header>
        <AlertDialog.Title>¿Eliminar {selectedTasks.size} {selectedTasks.size === 1 ? 'tarea' : 'tareas'}?</AlertDialog.Title>
        <AlertDialog.Description>
          Esta acción eliminará permanentemente las tareas seleccionadas. No se puede deshacer.
        </AlertDialog.Description>
      </AlertDialog.Header>
      <AlertDialog.Footer>
        <AlertDialog.Cancel>Cancelar</AlertDialog.Cancel>
        <AlertDialog.Action onclick={deleteSelectedTasks}>Eliminar</AlertDialog.Action>
      </AlertDialog.Footer>
    </AlertDialog.Content>
  </AlertDialog.Root>

  <!-- Dialog para editar tarea -->
  <Dialog.Root bind:open={showEditDialog}>
    <Dialog.Content class="edit-dialog-content">
      <Dialog.Header>
        <Dialog.Title>Editar Tarea</Dialog.Title>
        <Dialog.Description>
          Modifica los detalles de tu tarea.
        </Dialog.Description>
      </Dialog.Header>
      <div class="edit-form">
        <div class="form-field">
          <label for="edit-title">Título</label>
          <Input id="edit-title" bind:value={editTitle} placeholder="Título de la tarea" />
        </div>
        <div class="form-field">
          <label for="edit-priority">Prioridad</label>
          <select id="edit-priority" bind:value={editPriority} class="edit-select">
            <option value="low">Baja</option>
            <option value="medium">Media</option>
            <option value="high">Alta</option>
          </select>
        </div>
        <div class="form-field">
          <label for="edit-category">Categoría</label>
          <Input id="edit-category" bind:value={editCategory} placeholder="Categoría" />
        </div>
        <div class="form-field">
          <label for="edit-deadline">Fecha Límite (opcional)</label>
          <input id="edit-deadline" type="date" bind:value={editDeadline} class="edit-date-input" />
        </div>
      </div>
      <Dialog.Footer>
        <button class="dialog-btn cancel-btn" onclick={() => showEditDialog = false}>
          Cancelar
        </button>
        <button class="dialog-btn save-btn" onclick={saveEditTask}>
          Guardar
        </button>
      </Dialog.Footer>
    </Dialog.Content>
  </Dialog.Root>
  
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
</div>

<style>
/* --- LAYOUT & BASE --- */
.tasklist-container {
  min-height: 100vh;
  background: linear-gradient(160deg, #0a0e1a 0%, #141b2e 50%, #0f1420 100%);
  padding: 3rem 1.5rem;
  position: relative;
  overflow-x: hidden;
}

.main-content {
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  z-index: 10;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* --- HERO SECTION --- */
.page-hero {
  position: relative;
  padding: 3rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, rgba(255, 123, 84, 0.1) 0%, rgba(255, 178, 107, 0.05) 100%);
  border-radius: 24px;
  margin-bottom: 2.5rem;
  overflow: hidden;
}

.page-hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255, 123, 84, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 20s ease-in-out infinite;
}

.page-hero::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -5%;
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(255, 178, 107, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 15s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(20px, -20px) scale(1.1); }
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(15, 20, 36, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 123, 84, 0.3);
  border-radius: 50px;
  color: #ff7b54;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1rem;
  position: relative;
  z-index: 1;
}

.title-gradient {
  display: block;
  background: linear-gradient(120deg, #ff7b54, #ffb26b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-accent {
  display: block;
  color: #94a3b8;
  font-weight: 600;
  font-size: 2rem;
}

.hero-description {
  max-width: 600px;
  margin: 0 auto;
  color: #94a3b8;
  font-size: 1.125rem;
  line-height: 1.6;
  position: relative;
  z-index: 1;
}

/* --- STATS GRID --- */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2.5rem;
}

.stat-card {
  position: relative;
  background: rgba(15, 20, 36, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(125, 141, 166, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, #ff7b54, #ffb26b);
  opacity: 0;
  transition: opacity 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 123, 84, 0.4);
  box-shadow: 0 12px 32px rgba(255, 123, 84, 0.2);
}

.stat-card:hover::before {
  opacity: 1;
}



.stat-link {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  text-decoration: none;
  color: inherit;
  width: 100%;
}

.icon-bg {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  flex-shrink: 0;
  position: relative;
  transition: all 0.3s ease;
}

.icon-bg::after {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 12px;
  padding: 2px;
  background: linear-gradient(135deg, currentColor, transparent);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  opacity: 0.3;
}

.stat-card:hover .icon-bg {
  transform: scale(1.1);
}

.icon-bg.blue {
  background: rgba(99, 179, 237, 0.15);
  color: #63b3ed;
}

.icon-bg.green {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.icon-bg.red {
  background: rgba(255, 123, 84, 0.15);
  color: #ff7b54;
}

.icon-bg.purple {
  background: rgba(168, 139, 250, 0.15);
  color: #a78bfa;
}

.stat-data {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.stat-data.full-width {
  width: 100%;
}

.value {
  font-size: 2rem;
  font-weight: 700;
  color: #f7fafc;
  line-height: 1;
}

.value-small {
  font-size: 1.25rem;
  font-weight: 700;
  color: #f7fafc;
}

.label {
  font-size: 0.875rem;
  color: #94a3b8;
  font-weight: 500;
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-card {
  grid-column: span 2;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(125, 141, 166, 0.2);
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff7b54, #ffb26b);
  border-radius: 999px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 12px rgba(255, 123, 84, 0.5);
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .progress-card {
    grid-column: span 1;
  }
  
  .page-hero {
    padding: 2rem 1rem;
  }
  
  .hero-title {
    font-size: 2rem;
  }

  .title-accent {
    font-size: 1.5rem;
  }

  .hero-description {
    font-size: 1rem;
  }

  .add-task-form {
    padding: 1.5rem;
  }

  .task-input-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .task-input-row input[type="text"],
  .task-input-row select,
  .deadline-input-visible,
  .attach-btn,
  .submit-btn {
    width: 100%;
  }

  .task-input-row select {
    min-width: unset;
  }
}

/* --- ADD TASK FORM --- */
.add-task-form {
  background: rgba(20, 27, 46, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 123, 84, 0.15);
  border-radius: 24px;
  padding: 2rem;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
  animation: slideIn 0.5s ease-out 0.2s both;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.add-task-form:hover {
  border-color: rgba(255, 123, 84, 0.3);
  box-shadow: 0 10px 30px rgba(255, 123, 84, 0.1);
}

.task-input-row {
  display: grid;
  grid-template-columns: 1fr auto auto auto auto;
  gap: 0.875rem;
  align-items: center;
}

.task-input-row input[type="text"] {
  padding: 0.875rem 1.25rem;
  background: rgba(15, 20, 36, 0.8);
  border: 1.5px solid rgba(125, 141, 166, 0.2);
  border-radius: 16px;
  color: #f7fafc;
  font-size: 0.9375rem;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 500;
}

.task-input-row input[type="text"]:focus {
  border-color: rgba(255, 123, 84, 0.5);
  background: rgba(15, 20, 36, 1);
  box-shadow: 0 0 0 4px rgba(255, 123, 84, 0.1), 0 8px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.task-input-row input[type="text"]::placeholder {
  color: #4a5568;
  font-weight: 400;
}

.task-input-row select {
  padding: 0.875rem 1.25rem;
  background: rgba(15, 20, 36, 0.8);
  border: 1.5px solid rgba(125, 141, 166, 0.2);
  border-radius: 16px;
  color: #f7fafc;
  font-size: 0.9375rem;
  outline: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 150px;
  font-weight: 500;
}

.task-input-row select:hover {
  border-color: rgba(255, 123, 84, 0.3);
  background: rgba(15, 20, 36, 0.95);
}

.task-input-row select:focus {
  border-color: rgba(255, 123, 84, 0.5);
  background: rgba(15, 20, 36, 1);
  box-shadow: 0 0 0 4px rgba(255, 123, 84, 0.1);
  transform: translateY(-2px);
}

.task-input-row select option {
  background: #0f1424;
  color: #f7fafc;
  padding: 0.5rem;
}

.deadline-input-visible {
  padding: 0.875rem 1.25rem;
  background: linear-gradient(135deg, rgba(255, 123, 84, 0.15), rgba(255, 178, 107, 0.15));
  border: 1.5px solid rgba(255, 123, 84, 0.3);
  border-radius: 16px;
  color: #ff7b54;
  font-size: 0.9375rem;
  outline: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
}

.deadline-input-visible::-webkit-calendar-picker-indicator {
  filter: invert(0.6) sepia(1) saturate(5) hue-rotate(330deg);
  cursor: pointer;
}

.deadline-input-visible:hover {
  border-color: rgba(255, 123, 84, 0.5);
  background: linear-gradient(135deg, rgba(255, 123, 84, 0.2), rgba(255, 178, 107, 0.2));
  box-shadow: 0 4px 12px rgba(255, 123, 84, 0.2);
}

.deadline-input-visible:focus {
  border-color: rgba(255, 123, 84, 0.6);
  background: linear-gradient(135deg, rgba(255, 123, 84, 0.25), rgba(255, 178, 107, 0.25));
  box-shadow: 0 0 0 4px rgba(255, 123, 84, 0.15);
}

.attach-btn {
  padding: 0.875rem;
  background: rgba(255, 123, 84, 0.1);
  border: 1.5px solid rgba(255, 123, 84, 0.25);
  border-radius: 16px;
  color: #ff7b54;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.attach-btn:hover {
  background: rgba(255, 123, 84, 0.2);
  border-color: rgba(255, 123, 84, 0.5);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(255, 123, 84, 0.3);
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.875rem 1.75rem;
  background: linear-gradient(135deg, #ff7b54 0%, #ffb26b 100%);
  border: none;
  border-radius: 16px;
  color: #0a0e1a;
  font-size: 1.5rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  line-height: 1;
  box-shadow: 0 4px 20px rgba(255, 123, 84, 0.3);
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.submit-btn:hover::before {
  width: 300px;
  height: 300px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 12px 35px rgba(255, 123, 84, 0.5);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(-1px) scale(1.02);
}

.submit-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.files-wrapper-with-btn {
  width: 100%;
  margin-top: 1rem;
  position: relative;
  animation: fadeIn 0.3s ease-out;
}

.clear-files-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(252, 129, 129, 0.2);
  border: 1px solid rgba(252, 129, 129, 0.3);
  border-radius: 10px;
  color: #fc8181;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  z-index: 10;
  transition: all 0.2s ease;
}

.clear-files-btn:hover {
  background: rgba(252, 129, 129, 0.3);
  transform: scale(1.1);
}

.files-compact-preview {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 1rem;
  background: rgba(10, 14, 26, 0.6);
  border-radius: 16px;
  border: 1px solid rgba(125, 141, 166, 0.15);
}

.file-mini-item {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(20, 27, 46, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 123, 84, 0.2);
  transition: all 0.2s ease;
}

.file-mini-item:hover {
  transform: scale(1.05);
  border-color: rgba(255, 123, 84, 0.5);
}

.mini-preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mini-file-icon {
  font-size: 28px;
}

/* --- FILTER SECTION --- */
.filter-section-wrapper {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
  animation: slideIn 0.5s ease-out 0.3s both;
  position: relative;
  z-index: 50;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.complete-selected-btn,
.delete-selected-btn {
  padding: 0.875rem;
  border-radius: 16px;
  border: 1.5px solid;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
}

.complete-selected-btn {
  background: rgba(72, 187, 120, 0.1);
  border-color: rgba(72, 187, 120, 0.3);
  color: #48bb78;
}

.complete-selected-btn:hover {
  background: rgba(72, 187, 120, 0.2);
  border-color: #48bb78;
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(72, 187, 120, 0.3);
}

.delete-selected-btn {
  background: rgba(252, 129, 129, 0.1);
  border-color: rgba(252, 129, 129, 0.3);
  color: #fc8181;
}

.delete-selected-btn:hover {
  background: rgba(252, 129, 129, 0.2);
  border-color: #fc8181;
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(252, 129, 129, 0.3);
}

.filter-section {
  display: flex;
  gap: 1rem;
  flex: 1;
  position: relative;
  justify-content: flex-end;
  align-items: center;
  z-index: 100;
}

.select-all-btn {
  padding: 0;
  background: transparent;
  border: none;
  color: #ff7b54;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  letter-spacing: 0.01em;
}

.select-all-btn:hover:not(:disabled) {
  color: #ffb26b;
  text-decoration: underline;
}

.select-all-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.select-all-btn.all-selected {
  color: #48bb78;
}

.filter-trigger {
  padding: 0;
  background: transparent;
  border: none;
  color: #f7fafc;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-trigger:hover {
  color: #ff7b54;
  text-decoration: underline;
}

.filter-text {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-badge {
  padding: 0.25rem 0.75rem;
  background: rgba(255, 123, 84, 0.2);
  border-radius: 12px;
  font-size: 0.75rem;
  color: #ff7b54;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.chevron {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.chevron.open {
  transform: rotate(180deg);
}

.filter-dropdown {
  position: absolute;
  top: calc(100% + 0.75rem);
  left: auto;
  right: 0;
  background: #141b2e;
  backdrop-filter: blur(20px);
  border: 1.5px solid rgba(255, 123, 84, 0.3);
  border-radius: 20px;
  padding: 0.75rem;
  min-width: 220px;
  z-index: 1000;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
  animation: dropdownSlide 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes dropdownSlide {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  width: 100%;
  padding: 0.875rem 1.25rem;
  background: transparent;
  border: none;
  border-radius: 12px;
  color: #cbd5e1;
  font-size: 0.875rem;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.dropdown-item:hover {
  background: rgba(255, 123, 84, 0.1);
  color: #f7fafc;
  transform: translateX(4px);
}

.dropdown-item.active {
  background: rgba(255, 123, 84, 0.2);
  color: #ff7b54;
  font-weight: 700;
}

.priority-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 8px currentColor;
}

.priority-dot.high {
  background: #ff7b54;
}

.priority-dot.medium {
  background: #f6e05e;
}

.priority-dot.low {
  background: #63b3ed;
}

.priority-dot.overdue {
  background: #fc8181;
  animation: pulseDot 2s infinite;
}

@keyframes pulseDot {
  0%, 100% { 
    opacity: 1;
    transform: scale(1);
  }
  50% { 
    opacity: 0.6;
    transform: scale(1.2);
  }
}

/* --- SEARCH BAR --- */
.search-container {
  margin-bottom: 2rem;
  animation: slideIn 0.5s ease-out 0.4s both;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

:global(.search-icon) {
  position: absolute;
  left: 1.25rem;
  color: #7d8da6;
  pointer-events: none;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 1rem 3.5rem;
  background: rgba(20, 27, 46, 0.6);
  backdrop-filter: blur(20px);
  border: 1.5px solid rgba(125, 141, 166, 0.2);
  border-radius: 20px;
  color: #f7fafc;
  font-size: 0.9375rem;
  font-weight: 500;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.search-input:focus {
  border-color: rgba(255, 123, 84, 0.5);
  background: rgba(20, 27, 46, 0.8);
  box-shadow: 0 0 0 4px rgba(255, 123, 84, 0.1), 0 8px 24px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.search-input::placeholder {
  color: #4a5568;
  font-weight: 400;
}

.clear-search {
  position: absolute;
  right: 1.25rem;
  background: rgba(125, 141, 166, 0.1);
  border: none;
  color: #7d8da6;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.clear-search:hover {
  color: #cbd5e1;
  background: rgba(125, 141, 166, 0.2);
  transform: scale(1.1);
}

/* --- TASK LIST (MOBILE FIRST) --- */

.task-list-container {
  width: 100%;
  height: auto;
  overflow: visible;
  animation: slideIn 0.5s ease-out 0.5s both;
}

/* --- EDIT DIALOG STYLES --- */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin: 1.25rem 0;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.form-field label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #cbd5e1;
  letter-spacing: 0.01em;
}

:global(.edit-form input[data-slot="input"]) {
  background: rgba(15, 20, 36, 0.8) !important;
  border: 1.5px solid rgba(125, 141, 166, 0.2) !important;
  color: #f7fafc !important;
  border-radius: 14px !important;
  padding: 0.875rem 1.25rem !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
}

:global(.edit-form input[data-slot="input"]:focus) {
  border-color: rgba(255, 123, 84, 0.5) !important;
  box-shadow: 0 0 0 4px rgba(255, 123, 84, 0.1) !important;
  background: rgba(15, 20, 36, 1) !important;
}

.edit-select {
  width: 100%;
  padding: 0.875rem 1.25rem;
  border-radius: 14px;
  border: 1.5px solid rgba(125, 141, 166, 0.2);
  background: rgba(15, 20, 36, 0.8);
  color: #f7fafc;
  font-size: 0.875rem;
  font-weight: 500;
  outline: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.edit-select:focus {
  border-color: rgba(255, 123, 84, 0.5);
  box-shadow: 0 0 0 4px rgba(255, 123, 84, 0.1);
  background: rgba(15, 20, 36, 1);
}

.edit-select option {
  background: #0f1424;
  padding: 0.5rem;
}

.edit-date-input {
  width: 100%;
  padding: 0.875rem 1.25rem;
  border-radius: 14px;
  border: 1.5px solid rgba(125, 141, 166, 0.2);
  background: rgba(15, 20, 36, 0.8);
  color: #f7fafc;
  font-size: 0.875rem;
  font-weight: 500;
  outline: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.edit-date-input:focus {
  border-color: rgba(255, 123, 84, 0.5);
  box-shadow: 0 0 0 4px rgba(255, 123, 84, 0.1);
  background: rgba(15, 20, 36, 1);
}

.dialog-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 14px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  letter-spacing: 0.01em;
}

.cancel-btn {
  background: rgba(125, 141, 166, 0.1);
  color: #cbd5e1;
  border: 1.5px solid rgba(125, 141, 166, 0.2);
}

.cancel-btn:hover {
  background: rgba(125, 141, 166, 0.2);
  transform: translateY(-2px);
}

.save-btn {
  background: linear-gradient(135deg, #ff7b54, #ffb26b);
  color: #0a0e1a;
  box-shadow: 0 4px 20px rgba(255, 123, 84, 0.3);
}

.save-btn:hover {
  background: linear-gradient(135deg, #ff6b44, #ffa25b);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255, 123, 84, 0.5);
}

/* --- FLOATING AI BUTTON --- */
.floating-ai-btn {
  position: fixed;
  bottom: 2.5rem;
  right: 2.5rem;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff7b54, #ffb26b);
  border: none;
  color: #0a0e1a;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 12px 40px rgba(255, 123, 84, 0.5);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  animation: floatIn 0.6s ease-out 0.8s both;
}

@keyframes floatIn {
  from {
    opacity: 0;
    transform: translateY(100px) scale(0.5);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.floating-ai-btn:hover {
  transform: scale(1.15) rotate(10deg);
  box-shadow: 0 16px 50px rgba(255, 123, 84, 0.7);
}

.floating-ai-btn:active {
  transform: scale(1.05);
}

/* --- RESPONSIVE --- */
@media (max-width: 768px) {
  .tasklist-container {
    padding: 1.5rem 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .task-input-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .task-input-row input[type="text"],
  .task-input-row select,
  .attach-btn,
  .submit-btn {
    width: 100%;
  }

  .filter-section-wrapper {
    flex-direction: column;
  }

  .filter-section {
    width: 100%;
  }

  .select-all-btn,
  .filter-trigger {
    flex: 1;
  }

  .floating-ai-btn {
    width: 56px;
    height: 56px;
    bottom: 2rem;
    right: 2rem;
  }
}

</style>
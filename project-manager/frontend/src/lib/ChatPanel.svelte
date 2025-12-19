<script lang="ts">
	import { Bot, X, Send, Settings, Sparkles } from 'lucide-svelte';
	import { cn } from '$lib/utils';
	import { Button } from "$lib/components/ui/button/index.js";
	import { Input } from "$lib/components/ui/input/index.js";

	type Message = {
		role: 'user' | 'assistant';
		content: string;
		timestamp: Date;
	};

	let { 
		isOpen = $bindable(false),
		darkMode = false,
		taskId = undefined as number | undefined
	} = $props();

	let messages = $state<Message[]>([]);
	let inputMessage = $state('');
	let apiKey = $state('');
	let showSettings = $state(false);
	let isLoading = $state(false);

	const API_URL = 'https://br03lvnr-8000.usw3.devtunnels.ms/';

	$effect(() => {
		if (typeof window !== 'undefined') {
			const saved = localStorage.getItem('gemini_api_key');
			if (saved) apiKey = saved;
		}
	});

	function saveApiKey() {
		if (typeof window !== 'undefined') {
			localStorage.setItem('gemini_api_key', apiKey);
			showSettings = false;
		}
	}

	async function sendMessage() {
		if (!inputMessage.trim()) return;

		if (!apiKey || apiKey.trim() === '') {
			const errorMessage: Message = {
				role: 'assistant',
				content: '⚠️ No has configurado tu API key de Gemini. Haz clic en el ícono de configuración ⚙️ arriba para agregarla.',
				timestamp: new Date()
			};
			messages = [...messages, errorMessage];
			return;
		}

		const userMessage: Message = {
			role: 'user',
			content: inputMessage,
			timestamp: new Date()
		};

		messages = [...messages, userMessage];
		const currentMessage = inputMessage;
		inputMessage = '';
		isLoading = true;

		try {
			// Obtener token de localStorage
			const token = localStorage.getItem('access_token');
			const response = await fetch(`${API_URL}/api/chat`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					...(token ? { 'Authorization': `Bearer ${token}` } : {})
				},
				body: JSON.stringify({
					message: currentMessage,
					task_id: taskId,
					api_key: apiKey
				})
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({ detail: 'Error desconocido' }));
				throw new Error(errorData.detail || 'Error al comunicarse con la IA');
			}

			const data = await response.json();

			const aiMessage: Message = {
				role: 'assistant',
				content: data.response,
				timestamp: new Date()
			};

			messages = [...messages, aiMessage];
		} catch (error) {
			const errorMessage: Message = {
				role: 'assistant',
				content: `Error: ${error instanceof Error ? error.message : 'No se pudo conectar con la IA'}`,
				timestamp: new Date()
			};
			messages = [...messages, errorMessage];
		} finally {
			isLoading = false;
		}
	}

	function handleKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			sendMessage();
		}
	}
</script>

{#if isOpen}
	<!-- Overlay -->
	<div 
		class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm"
		onclick={() => isOpen = false}
		onkeydown={(e) => e.key === 'Escape' && (isOpen = false)}
		role="button"
		tabindex="0"
		aria-label="Close chat"
	></div>

	<!-- Panel -->
	<div class={cn(
		"fixed inset-y-0 right-0 z-50 w-full max-w-md border-l bg-background p-0 shadow-lg transition-transform duration-300 ease-in-out sm:max-w-lg",
		isOpen ? "translate-x-0" : "translate-x-full"
	)}>
		<!-- Header -->
		<div class="flex items-center justify-between border-b px-6 py-4">
			<div class="flex items-center gap-3">
				<div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary">
					<Sparkles class="h-5 w-5" />
				</div>
				<div>
					<h3 class="font-semibold leading-none tracking-tight">AI Assistant</h3>
					<p class="text-sm text-muted-foreground">Smart project assistant</p>
				</div>
			</div>
			<div class="flex items-center gap-2">
				<Button variant="ghost" size="icon" onclick={() => showSettings = !showSettings} aria-label="Settings">
					<Settings class="h-4 w-4" />
				</Button>
				<Button variant="ghost" size="icon" onclick={() => isOpen = false} aria-label="Close">
					<X class="h-4 w-4" />
				</Button>
			</div>
		</div>

		<!-- Settings Panel -->
		{#if showSettings}
			<div class="border-b bg-muted/50 px-6 py-4">
				<div class="space-y-3">
					<div class="space-y-1">
						<label for="api-key" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
							Google Gemini API Key
						</label>
						<Input 
							id="api-key"
							type="password" 
							bind:value={apiKey} 
							placeholder="AIza..." 
							class="font-mono"
						/>
					</div>
					<Button onclick={saveApiKey} size="sm" class="w-full">
						Save API Key
					</Button>
					<p class="text-xs text-muted-foreground">
						Get your API key for FREE at <a href="https://makersuite.google.com/app/apikey" target="_blank" class="text-primary hover:underline">Google AI Studio</a>
					</p>
				</div>
			</div>
		{/if}

		<!-- Messages -->
		<div class="flex flex-1 flex-col gap-4 overflow-y-auto p-6 h-[calc(100vh-180px)]">
			{#if messages.length === 0}
				<div class="flex flex-col items-center justify-center gap-4 py-10 text-center text-muted-foreground">
					<div class="rounded-full bg-muted p-4">
						<Bot class="h-8 w-8" />
					</div>
					<div class="space-y-1">
						<h4 class="font-medium text-foreground">Hello! I'm your AI assistant</h4>
						<p class="text-sm">Ask me anything about your project or tasks.</p>
					</div>
					{#if taskId}
						<div class="inline-flex items-center gap-1.5 rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
							<Sparkles class="h-3 w-3" />
							Task Context Active
						</div>
					{/if}
				</div>
			{:else}
				{#each messages as message}
					<div class={cn("flex w-full gap-3", message.role === 'user' ? "flex-row-reverse" : "flex-row")}>
						<div class={cn(
							"flex h-8 w-8 shrink-0 items-center justify-center rounded-full border",
							message.role === 'assistant' ? "bg-primary text-primary-foreground border-primary" : "bg-muted text-muted-foreground"
						)}>
							{#if message.role === 'user'}
								<span class="text-xs font-bold">You</span>
							{:else}
								<Bot class="h-4 w-4" />
							{/if}
						</div>
						<div class={cn(
							"flex max-w-[80%] flex-col gap-1",
							message.role === 'user' ? "items-end" : "items-start"
						)}>
							<div class={cn(
								"rounded-2xl px-4 py-2.5 text-sm shadow-sm",
								message.role === 'user' 
									? "bg-primary text-primary-foreground rounded-tr-none" 
									: "bg-muted text-foreground rounded-tl-none"
							)}>
								{message.content}
							</div>
							<span class="text-[10px] text-muted-foreground">
								{message.timestamp.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}
							</span>
						</div>
					</div>
				{/each}
			{/if}

			{#if isLoading}
				<div class="flex w-full gap-3">
					<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
						<Bot class="h-4 w-4" />
					</div>
					<div class="flex items-center gap-1 rounded-2xl rounded-tl-none bg-muted px-4 py-3">
						<span class="h-1.5 w-1.5 animate-bounce rounded-full bg-foreground/50 [animation-delay:-0.3s]"></span>
						<span class="h-1.5 w-1.5 animate-bounce rounded-full bg-foreground/50 [animation-delay:-0.15s]"></span>
						<span class="h-1.5 w-1.5 animate-bounce rounded-full bg-foreground/50"></span>
					</div>
				</div>
			{/if}
		</div>

		<!-- Input -->
		<div class="absolute bottom-0 left-0 right-0 border-t bg-background p-4">
			{#if !apiKey}
				<div class="mb-3 flex items-center gap-2 rounded-lg bg-yellow-500/10 px-3 py-2 text-xs font-medium text-yellow-600 dark:text-yellow-500">
					<Settings class="h-3 w-3" />
					Configure your API key to start chatting
				</div>
			{/if}
			<div class="flex gap-2">
				<textarea
					bind:value={inputMessage}
					onkeydown={handleKeyDown}
					placeholder={apiKey ? "Type your message..." : "Configure API key first"}
					disabled={!apiKey || isLoading}
					rows="1"
					class="flex min-h-11 w-full resize-none rounded-xl border border-input bg-background px-3 py-2.5 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
				></textarea>
				<Button 
					onclick={sendMessage}
					disabled={!inputMessage.trim() || !apiKey || isLoading}
					size="icon"
					class="h-11 w-11 shrink-0 rounded-xl"
				>
					<Send class="h-4 w-4" />
				</Button>
			</div>
		</div>
	</div>
{/if}

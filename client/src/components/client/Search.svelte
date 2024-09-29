<script lang="ts">
	import SearchIcon from '@/clientComponents/SearchIcon'
	import Modal from './Modal.svelte'
	import { clientFetchLink } from 'src/utils/config'
	import { debounce } from 'src/utils/minLodash'
	import type { GetPostListResponse } from '@/types/responses'

	let showModal: boolean = false
	let loading: boolean = false
	let results: GetPostListResponse[] = []
	let searchContext: string = ''

	const searchPosts = async () => {
		try {
			const res = await fetch(`${clientFetchLink}/posts?match_search=${searchContext}&per_page=50`)
			if (!res.ok) new Error('aaa')
			const posts = await res.json()
			results = posts
		} catch (e) {
			console.log(e)
		} finally {
			loading = false
		}
	}
</script>

<button
	class="flex items-center justify-center rounded-md gap-1"
	on:click={() => (showModal = true)}
>
	<SearchIcon />
</button>

<Modal bind:showModal>
	<input
		class="h-12 w-full px-4 border-2 border-black rounded-md"
		type="text"
		placeholder="Search"
		bind:value={searchContext}
		on:input={debounce(searchPosts, 850)}
		on:input={() => {
			if (searchContext.length) loading = true
			else results = []
		}}
	/>
	{#if loading}
		<h3 class="mt-4 pl-2">Searching for "{searchContext}"...</h3>
	{:else if !loading && !results.length && searchContext.length}
		<h3 class="mt-4 pl-2">No result for "{searchContext}"</h3>
	{:else}
		{#if !loading && results.length}
			<h3 class="mt-4 pl-2 text-xl font-bold">Result for "{searchContext}"</h3>
		{/if}
		<ol class="definition-list mt-5">
			{#each results as post}
				<li class="mb-2">
					<a
						class="flex flex-col items-center bg-white border border-gray-200 rounded-lg md:flex-row hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700"
						target="_blank"
						rel="noreferrer"
						href="posts/{post.id}"
					>
						<img
							class="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-s-lg"
							src={post.banner_img}
							alt=""
						/>
						<div class="flex flex-col justify-between p-4 leading-normal">
							<span class="mb-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white">
								{post.title}
							</span>
						</div>
					</a>
				</li>
			{/each}
		</ol>
	{/if}
</Modal>

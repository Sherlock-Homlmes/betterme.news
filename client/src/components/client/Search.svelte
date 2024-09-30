<script lang="ts">
	import SearchIcon from '@/clientComponents/SearchIcon'
	import Modal from './Modal.svelte'
	import { clientFetchLink } from 'src/utils/config'
	import { debounce } from 'src/utils/minLodash'
	import type { GetPostListResponse } from '@/types/responses'

	let showModal: boolean = false
	let loading: boolean = false
	let results: GetPostListResponse[] = []
	let searchContextModel: string = ''
	$: searchContext = searchContextModel.trim()
	let previousSearchContext: string = ''
	let shouldShowMoreButton: boolean = false

	const searchPosts = async () => {
		if (!searchContext.length) {
			results = []
			return
		}
		if (searchContext === previousSearchContext) {
			loading = false
			return
		}
		try {
			const res = await fetch(`${clientFetchLink}/posts?match_search=${searchContext}&per_page=20`)
			if (!res.ok) new Error('API error')
			const posts = await res.json()
			previousSearchContext = searchContext
			results = posts
			if (results.length >= 20) shouldShowMoreButton = true
			// TODO: fail to check header
			// const totalPostsCount: number = parseInt(res.headers.get('x-total-count'))
			// if (totalPostsCount > 20) shouldShowMoreButton = true
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
		autofocus
		class="h-12 w-full px-4 border-2 border-black rounded-md"
		type="text"
		placeholder="Search"
		bind:value={searchContextModel}
		on:input={debounce(searchPosts, 850)}
		on:input={() => {
			if (searchContext.length) loading = true
			else results = []
		}}
	/>
	{#if loading}
		<h3 class="my-4 pl-2">Tìm kiếm kết quả cho "{searchContext}"...</h3>
	{:else if !loading && !results.length && searchContext.length}
		<h3 class="my-4 pl-2">Không có kết quả cho "{searchContext}"</h3>
	{:else if !loading && results.length}
		<h3 class="mt-4 pl-2 text-xl font-bold">Kết quả cho "{searchContext}"</h3>
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
		{#if shouldShowMoreButton}
			<div class="flex justify-center">
				<a href={`/search?match_search=${searchContext}`} class="mt-3">
					<button
						class="bg-black text-white p-3 rounded-full mb-4 dark:text-black dark:bg-white text-underline hover:scale-105"
					>
						Hiển thị thêm
					</button>
				</a>
			</div>
		{/if}
	{:else if !loading}
		<div class="mb-8"></div>
	{/if}
</Modal>

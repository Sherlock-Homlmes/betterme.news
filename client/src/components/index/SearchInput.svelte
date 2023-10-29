<script>
  import { Search, Button, Dropdown, DropdownItem } from "flowbite-svelte";
  import "iconify-icon";

  const items = [
    {
      label: "All categories",
    },
    {
      label: "Mockups",
    },
    {
      label: "Templates",
    },
    {
      label: "Design",
    },
    {
      label: "Logos",
    },
  ];

  let selectCategory = "All categories";
</script>

<form class="flex w-[700px]">
  <div class="relative">
    <Button
      class=" w-[150px] rounded-e-none whitespace-nowrap border border-r-0 border-primary-700"
    >
      {selectCategory}
      <iconify-icon icon="mdi:chevron-down" class="w-2.5 h-2.5 ml-2.5" />
    </Button>
    <Dropdown classContainer="w-40">
      {#each items as { label }}
        <DropdownItem
          on:click={() => {
            selectCategory = label;
          }}
          class={selectCategory === label ? "underline" : ""}
        >
          {label}
        </DropdownItem>
      {/each}
    </Dropdown>
  </div>
  <Search
    size="md"
    class="rounded-none py-2.5"
    placeholder="Search Mockups, Logos, Design Templates..."
  />
  <Button class="!p-2.5 rounded-s-none">
    <iconify-icon icon="mdi:magnify" class="w-5 h-5" />
  </Button>
</form>

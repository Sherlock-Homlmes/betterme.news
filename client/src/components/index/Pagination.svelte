<script>
  import { currentPage } from "./store";

  import { Pagination } from "flowbite-svelte";

  let pages = [
    { name: 1, href: "?page=1" },
    { name: 2, href: "?page=2" },
    { name: 3, href: "?page=3" },
    { name: 4, href: "?page=4" },
    { name: 5, href: "?page=5" },
  ];

  $: {
    pages.forEach((page) => {
      let splitUrl = page.href.split("?");
      let queryString = splitUrl.slice(1).join("?");
      const hrefParams = new URLSearchParams(queryString);
      let hrefValue = hrefParams.get("page");
      if (hrefValue === currentPage.get()) {
        page.active = true;
      } else {
        page.active = false;
      }
    });
    pages = pages;
  }

  const previous = () => {
    alert("Previous btn clicked. Make a call to your server to fetch data.");
  };
  const next = () => {
    alert("Next btn clicked. Make a call to your server to fetch data.");
  };
</script>

<Pagination {pages} large on:previous={previous} on:next={next} />

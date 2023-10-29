<script>
  import { Card } from "flowbite-svelte";
  export let reverse = false;
  export let horizontal = false;
  export let title = "Noteworthy technology acquisitions 2021";
  export let description = "";
  export let image =
    "https://cdn4.ivolunteer.vn/post/wp-content/uploads/2023/10/27225259/Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-14-3.png";
  export let textSize = "xl";
  // grayscale hover:grayscale-0 hover:scale-105
</script>

<div>
  <Card img={image} href="/" padding="md" {horizontal} {reverse} class="mb-4">
    <h6
      class="mb-2 text-{textSize} font-bold tracking-tight text-slate-900 dark:text-white"
    >
      {title}
    </h6>
    <p>{description}</p>
  </Card>
</div>

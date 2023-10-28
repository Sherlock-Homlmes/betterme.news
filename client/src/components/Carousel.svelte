<script>
  import { Carousel } from "flowbite-svelte";

  let index = 0;
  const images = [
    {
      alt: "Câu Lạc Bộ Pháp Ngữ Học Viên Ngoại Giao Chính Thức Mở Đơn Tuyển Thành Viên",
      src: "https://cdn4.ivolunteer.vn/post/wp-content/uploads/2023/10/27225259/Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-14-3.png",
      title: "cosmic-timetraveler-pYyOZ8q7AII-unsplash.com",
    },
    {
      alt: "Câu Lạc Bộ Pháp Ngữ Học Viên Ngoại Giao Chính Thức Mở Đơn Tuyển Thành Viên",
      src: "https://cdn4.ivolunteer.vn/post/wp-content/uploads/2023/10/27225259/Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-14-3.png",
      title: "cristina-gottardi-CSpjU6hYo_0-unsplash.com",
    },
    {
      alt: "Câu Lạc Bộ Pháp Ngữ Học Viên Ngoại Giao Chính Thức Mở Đơn Tuyển Thành Viên",
      src: "https://cdn4.ivolunteer.vn/post/wp-content/uploads/2023/10/27225259/Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-14-3.png",
      title: "johannes-plenio-RwHv7LgeC7s-unsplash.com",
    },
    {
      alt: "Câu Lạc Bộ Pháp Ngữ Học Viên Ngoại Giao Chính Thức Mở Đơn Tuyển Thành Viên",
      src: "https://cdn4.ivolunteer.vn/post/wp-content/uploads/2023/10/27225259/Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-14-3.png",
      title: "jonatan-pie-3l3RwQdHRHg-unsplash.com",
    },
    {
      alt: "Câu Lạc Bộ Pháp Ngữ Học Viên Ngoại Giao Chính Thức Mở Đơn Tuyển Thành Viên",
      src: "https://cdn4.ivolunteer.vn/post/wp-content/uploads/2023/10/27225259/Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-14-3.png",
      title: "mark-harpur-K2s_YE031CA-unsplash",
    },
    {
      alt: "Câu Lạc Bộ Pháp Ngữ Học Viên Ngoại Giao Chính Thức Mở Đơn Tuyển Thành Viên",
      src: "https://cdn4.ivolunteer.vn/post/wp-content/uploads/2023/10/27225259/Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-14-3.png",
      title: "pietro-de-grandi-T7K4aEPoGGk-unsplash",
    },
    {
      alt: "Câu Lạc Bộ Pháp Ngữ Học Viên Ngoại Giao Chính Thức Mở Đơn Tuyển Thành Viên",
      src: "https://cdn4.ivolunteer.vn/post/wp-content/uploads/2023/10/27225259/Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-14-3.png",
      title: "sergey-pesterev-tMvuB9se2uQ-unsplash",
    },
    {
      alt: "Câu Lạc Bộ Pháp Ngữ Học Viên Ngoại Giao Chính Thức Mở Đơn Tuyển Thành Viên",
      src: "https://cdn4.ivolunteer.vn/post/wp-content/uploads/2023/10/27225259/Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-14-3.png",
      title: "solotravelgoals-7kLufxYoqWk-unsplash",
    },
  ];
  let image;
</script>

<div class="max-w-4xl space-y-4">
  <Carousel
    {images}
    let:Indicators
    let:Controls
    on:change={({ detail }) => (image = detail)}
  >
    <Controls />
    <Indicators />
  </Carousel>

  <div
    class="rounded h-10 bg-gray-300 dark:bg-gray-700 dark:text-white p-2 my-2 text-center"
  >
    {image?.alt}
  </div>
</div>

let isContentChanged = false;

const onContentChange = () => {
  console.log("change");
  isContentChanged = true;
  document.getElementById("send-post-btn").style.display = "none";
};

const getCurrentData = () => {
  const discordContent = [];
  for (var i = 1; i <= discordContentLength; i++) {
    discordContent.push(
      document.getElementById(`discord-content-item-${i}`).value,
    );
  }

  return {
    origin: origin,
    post_name: postName,

    banner:
      getImageFromElement("banner-img") === null
        ? null
        : getImageFromElement("banner-img"),
    thumbnail:
      getImageFromElement("thumbnail-img") === null
        ? null
        : getImageFromElement("thumbnail-img"),

    discord_content: discordContent,
    discord_description: document.getElementById("description").value,

    html_content: "",
    html_description: "",
  };
};

const getImageFromElement = (imgId) => {
  var file = document.getElementById(imgId).files;
  return file && file.length > 0 ? file[0] : null;
};

// TODO: rewrite this
const previewImage = () => {
  const bannerImage = getImageFromElement("banner-input");
  const thumnailImage = getImageFromElement("thumbnail-input");
  if (bannerImage !== null) {
    var fileReader = new FileReader();
    fileReader.onload = (event) => {
      document
        .getElementById("banner-image")
        .setAttribute("src", event.target.result);
    };
    fileReader.readAsDataURL(bannerImage);
  }
  if (thumnailImage !== null) {
    var fileReader = new FileReader();
    fileReader.onload = (event) => {
      document
        .getElementById("thumbnail-image")
        .setAttribute("src", event.target.result);
    };
    fileReader.readAsDataURL(thumnailImage);
  }
  onContentChange();
};

// Save test post to discord and facebook
const sendTestPost = async () => {
  const currentData = getCurrentData();
  currentData.is_testing = true;

  const response = await fetch("/api/crawlers/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(currentData),
  });

  document.getElementById("send-post-btn").style.display = "block";
};

// Save post to production
const sendPost = async () => {
  const currentData = getCurrentData();
  currentData.is_testing = false;

  const response = await fetch("/api/crawlers/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(currentData),
  });
};

// Save current post to draft
const savePost = async () => {
  const currentData = getCurrentData();
  // fetch data
  await fetch(`/api/crawlers/${postName}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(currentData),
  });
  isContentChanged = false;
};

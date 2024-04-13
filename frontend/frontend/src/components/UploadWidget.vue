<template>
  <div class="uw">
    <button v-on:click="open" id="upload_widget" class="cloudinary-button">
      Upload Cover
    </button>
  </div>
</template>

<script>
export default {
  name: "UploadWidget",
  mounted() {
    const cloudName = "hzxyensd5";
    const uploadPreset = "aoh4fpwm";

    const myWidget = cloudinary.createUploadWidget(
      {
        cloudName: cloudName,
        uploadPreset: uploadPreset,
      },
      (error, result) => {
        if (!error && result && result.event === "success") {
          console.log("Done! Here is the image info: ", result.info);
          document
            .getElementById("uploadedimage")
            .setAttribute("src", result.info.secure_url);
          this.setUrl(result.info.secure_url);
        }
      }
    );

    this.myWidget = myWidget;
  },
  data() {
    return {
      myWidget: null,
    };
  },
  props: {
    msg: String,
  },
  methods: {
    open() {
      this.myWidget.open();
    },
    setUrl(url) {
      this.$emit("incomingUrl", url);
    },
  },
};
</script>

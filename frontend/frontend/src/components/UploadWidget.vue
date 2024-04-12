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
    const cloudName = "hzxyensd5"; // replace with your own cloud name
    const uploadPreset = "aoh4fpwm"; // replace with your own upload preset

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

    // Assign myWidget to a data property for access inside methods
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
      // Call open on myWidget
      this.myWidget.open();
    },
    setUrl(url) {
      this.$emit("incomingUrl", url);
    },
  },
};
</script>

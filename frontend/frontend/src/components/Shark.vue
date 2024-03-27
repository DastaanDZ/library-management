<template>
  <div>
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Shark",
  data() {
    return {
      msg: "",
    };
  },
  methods: {
    getResponse() {
      const path = "http://127.0.0.1:5000/shark";
      axios
        .get(path)
        .then((result) => {
          console.log(result.data);
          this.msg = result.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },

  created() {
    this.getResponse();
  },
};
</script>

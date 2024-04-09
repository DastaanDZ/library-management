<template>
  <div class="button-group-page">
    <!-- Added button group -->
    <div class="btn-group" role="group" aria-label="Basic example">
      <button
        type="button"
        class="btn btn-primary"
        @click="redirectTo('/add-book')"
      >
        Add Book
      </button>
      <button
        type="button"
        class="btn btn-primary"
        @click="redirectTo('/monitor')"
      >
        Monitor
      </button>
      <button
        type="button"
        class="btn btn-primary"
        @click="redirectTo('/add-section')"
      >
        Add Section
      </button>
      <button
        type="button"
        class="btn btn-primary"
        @click="redirectTo('/assign-section')"
      >
        Assign Section
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "LibrarianAction",
  methods: {
    redirectTo(path) {
      this.$router.push(path);
    },
  },
};
</script>

<style scoped>
.button-group-page {
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-group {
  display: flex;
}

.btn-group button {
  margin: 0 5px;
}
</style>

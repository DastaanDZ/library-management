To make the navbar span redirect to /user if the role is user, and /librarian if
the role is not user, you can use Vue Router's programmatic navigation inside a
method. Here's how you can do it: vue Copy code
<template>
  <nav class="navbar navbar-light bg-light">
    <div class="container-fluid">
      <span class="navbar-brand mb-0 h1" @click="redirectToRolePage"
        >Library App</span
      >
    </div>
  </nav>
</template>

<script>
export default {
  name: "Navbar",
  methods: {
    redirectToRolePage() {
      const role = localStorage.getItem("role");
      if (role === "user") {
        this.$router.push("/user");
      } else {
        this.$router.push("/librarian");
      }
    },
  },
};
</script>

<style>
.navbar-brand:hover {
  cursor: pointer;
}
</style>

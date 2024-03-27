<template>
  <div class="vue-tempalte">
    <Navbar />
    <form @submit.prevent="submitForm">
      <h3>Sign In</h3>
      <div class="mb-3">
        <label>Username</label>
        <input
          v-model.trim="username"
          type="text"
          class="form-control form-control-lg"
        />
      </div>
      <div class="mb-3">
        <label>Password</label>
        <input
          v-model.trim="password"
          type="password"
          class="form-control form-control-lg"
        />
      </div>
      <button type="submit" class="btn btn-dark btn-lg btn-block">
        Sign In
      </button>
      <p class="forgot-password text-right mt-2 mb-4">
        <router-link to="/forgot-password">Forgot password ?</router-link>
      </p>
      <div class="social-icons">
        <ul>
          <li>
            <a href="#"><i class="fa fa-google"></i></a>
          </li>
          <li>
            <a href="#"><i class="fa fa-facebook"></i></a>
          </li>
          <li>
            <a href="#"><i class="fa fa-twitter"></i></a>
          </li>
        </ul>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "./Navbar.vue";

export default {
  components: {
    Navbar,
  },
  data() {
    return {
      username: "", // Changed from email to username
      password: "",
    };
  },
  methods: {
    submitForm() {
      // Prepare the form data object
      const formData = {
        username: this.username,
        password: this.password,
      };

      // Make an HTTP POST request to the backend route
      const path = "http://127.0.0.1:5000/login";
      axios
        .post(path, formData)
        .then((response) => {
          console.log(response.data.access_token); // Log the access token
          // Optionally, you can store the access token in local storage or Vuex store
          // Redirect the user to another route upon successful login
          this.$router.push("/dashboard");
        })
        .catch((error) => {
          console.error("Error:", error); // Log any errors
          // Display an error message to the user
          alert("Invalid username or password. Please try again.");
        });
    },
  },
};
</script>

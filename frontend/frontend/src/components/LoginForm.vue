<template>
  <div class="vue-tempalte">
    <Navbar />
    <div class="main-div">
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
          New User
          <router-link :to="{ name: 'RegisterForm' }">sign up?</router-link>
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
      username: "",
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
          // Check if access token is present in the response data
          if (response.data && response.data.access_token) {
            // Store the access token in localStorage
            localStorage.setItem("accessToken", response.data.access_token);
            console.log("token set in local storage");
            // Redirect to the dashboard after successful login
            this.$router.push("/user-info");
          } else {
            // Handle case where access token is missing or invalid
            console.error("Access token not found in response data");
            alert("Invalid response from the server. Please try again.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Invalid username or password. Please try again.");
        });
    },
  },
};
</script>

<style scoped>
.main-div {
  width: 100%;
  height: 70vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
form {
  display: flex;
  flex-direction: column;
  width: fit-content;
}
</style>

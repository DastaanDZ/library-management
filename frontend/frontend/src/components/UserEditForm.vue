<template>
  <div class="registration-form">
    <form @submit.prevent="saveChanges">
      <div class="form-icon">
        <span><i class="icon icon-user"></i></span>
      </div>
      <div class="form-group">
        <input
          v-model="userData.username"
          type="text"
          class="form-control item"
          id="username"
          placeholder="Username"
        />
      </div>
      <div class="form-group">
        <input
          v-model="userData.password"
          type="password"
          class="form-control item"
          id="password"
          placeholder="Password"
        />
      </div>
      <div class="form-group">
        <input
          v-model="userData.email"
          type="text"
          class="form-control item"
          id="email"
          placeholder="Email"
        />
      </div>
      <div class="form-group">
        <input
          v-model="userData.role"
          type="text"
          class="form-control item"
          id="role"
          placeholder="role"
        />
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-block create-account">
          Save Changes
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default {
  name: "UserEditForm",
  data() {
    return {
      userData: {
        username: "",
        password: "",
        email: "",
        role: "",
      },
    };
  },
  methods: {
    async saveChanges() {
      try {
        // Retrieve access token from localStorage
        const accessToken = localStorage.getItem("accessToken");

        if (!accessToken) {
          throw new Error("Access token not found");
        }

        // Decode the access token to extract user ID
        const decodedToken = jwtDecode(accessToken);
        console.log(decodedToken);
        const userId = decodedToken.sub;

        // Check if user ID is valid
        if (!userId) {
          throw new Error("Invalid user ID");
        }

        // Make PUT request to update user data
        const response = await axios.put(
          `http://127.0.0.1:5000/edit-user/${userId}`,
          this.userData
        );
        console.log(response.data);
        // Optionally, you can show a success message or redirect the user after successful update
      } catch (error) {
        console.error("Error updating user:", error);
        // Handle error - e.g., show an error message to the user
        if (error.response && error.response.status === 401) {
          // Unauthorized access, redirect to login page
          this.$router.push("/login");
        } else {
          // Other errors, redirect to user info page
          this.$router.push("/user-info");
        }
      }
    },
  },
};
</script>

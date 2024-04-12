<template>
  <div class="edit-profile-form">
    <h1>EDIT PROFILE</h1>
    <form @submit.prevent="saveChanges">
      <div class="form-group text-start mb-1">
        <label for="username">Username:</label>
        <input
          v-model="userData.username"
          type="text"
          class="form-control item"
          id="username"
          placeholder="Username"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="password">Password:</label>
        <input
          v-model="userData.password"
          type="password"
          class="form-control item"
          id="password"
          placeholder="Password"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="email">Email:</label>
        <input
          v-model="userData.email"
          type="text"
          class="form-control item"
          id="email"
          placeholder="Email"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="role">Role:</label>
        <input
          v-model="userData.role"
          type="text"
          class="form-control item"
          id="role"
          placeholder="Role"
        />
      </div>
      <div class="form-group text-start mb-1">
        <button type="submit" class="btn btn-block save-changes">
          Save Changes
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditProfileForm",
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
  mounted() {
    this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/user-info/${this.$route.params.userId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.userData = response.data;
      } catch (error) {
        console.error("Error fetching user info:", error);
        if (error.response && error.response.status === 404) {
          // Redirect to login page if unauthorized (status code 404)
          this.$router.push("/login");
        }
      }
    },
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
          `http://127.0.0.1:5000/edit-user/${this.$route.params.userId}`,
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

<style scoped>
.edit-profile-form {
  padding: 50px 0;
}

.edit-profile-form form {
  background-color: #fff;
  max-width: 600px;
  margin: auto;
  padding: 50px 70px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.edit-profile-form .form-group {
  margin-bottom: 20px;
}

.edit-profile-form .item {
  border-radius: 20px;
  padding: 10px 20px;
}

.edit-profile-form .save-changes {
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 18px;
  font-weight: bold;
  background-color: #5791ff;
  border: none;
  color: white;
  margin-top: 20px;
}

@media (max-width: 576px) {
  .edit-profile-form form {
    padding: 50px 20px;
  }
}
</style>

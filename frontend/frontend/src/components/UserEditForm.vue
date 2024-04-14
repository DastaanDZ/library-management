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
        <button type="submit" class="btn btn-block save-changes">
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
        const accessToken = localStorage.getItem("accessToken");

        if (!accessToken) {
          console.error("Access token not found in localStorage");
          return;
        }

        const decodedToken = jwtDecode(accessToken);
        const user_id = decodedToken.sub;
        const response = await axios.get(
          `http://127.0.0.1:5000/user-info/${user_id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.userData = response.data;
      } catch (error) {
        console.error("Error fetching user info:", error);
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
      }
    },
    async saveChanges() {
      try {
        const accessToken = localStorage.getItem("accessToken");

        if (!accessToken) {
          throw new Error("Access token not found");
        }
        const decodedToken = jwtDecode(accessToken);
        console.log(decodedToken);
        const userId = decodedToken.sub;

        if (!userId) {
          throw new Error("Invalid user ID");
        }

        const response = await axios.put(
          `http://127.0.0.1:5000/edit-user/${userId}`,
          this.userData
        );
        console.log(response.data);
        if (localStorage.getItem("role") == "librarian") {
          this.$router.push("/librarian");
        } else {
          this.$router.push("/user");
        }
      } catch (error) {
        console.error("Error updating user:", error);
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        } else {
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

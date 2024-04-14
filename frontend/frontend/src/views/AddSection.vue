<template>
  <div class="add-section-page">
    <h1>Add Section</h1>
    <form @submit.prevent="addSection">
      <div class="form-group text-start mb-1">
        <label for="name">Name:</label>
        <input
          v-model="sectionData.name"
          type="text"
          class="form-control item"
          id="name"
          placeholder="Section Name"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="description">Description:</label>
        <textarea
          v-model="sectionData.description"
          class="form-control item"
          id="description"
          rows="5"
          placeholder="Section Description"
        ></textarea>
      </div>
      <div class="form-group text-start mb-1">
        <button type="submit" class="btn btn-primary create-section">
          Add Section
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddSection",
  data() {
    return {
      sectionData: {
        name: "",
        description: "",
      },
    };
  },
  methods: {
    async addSection() {
      try {
        const accessToken = localStorage.getItem("accessToken");

        const response = await axios.post(
          "http://127.0.0.1:5000/add-section",
          this.sectionData,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        console.log(response.data.message);
        console.log("New section ID:", response.data.section_id);

        alert("Section Added");

        this.sectionData.name = "";
        this.sectionData.description = "";
      } catch (error) {
        if (error.response && error.response.status === 400) {
          alert("Missing data required");
        }
        console.error("Error adding section:", error);
      }
    },
  },
};
</script>

<style>
.add-section-page {
  padding: 50px 0;
}

.add-section-page form {
  background-color: #fff;
  max-width: 600px;
  margin: auto;
  padding: 50px 70px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.add-section-page .form-group {
  margin-bottom: 20px;
}

.add-section-page .item {
  border-radius: 20px;
  padding: 10px 20px;
}

.add-section-page .create-section {
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 18px;
  font-weight: bold;
  background-color: #5791ff;
  border: none;
  color: white;
  margin-top: 20px;
}
</style>

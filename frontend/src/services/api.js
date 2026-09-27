import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    Accept: "application/json",
  },
});

export const recommendJobsFromCV = async ({
  file,
  preferredRole,
  preferredLocation,
}) => {
  const formData = new FormData();

  formData.append("file", file);
  formData.append(
    "preferred_role",
    preferredRole
  );
  formData.append(
    "preferred_location",
    preferredLocation
  );

  const response = await api.post(
    "/jobs/recommend-from-cv",
    formData
  );

  return response.data;
};

export default api;
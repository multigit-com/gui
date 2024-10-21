const initialState = {
  files: [],
  loading: false,
  error: null,
};

export const repositoryReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'FETCH_REPOSITORY_FILES_START':
      return { ...state, loading: true, error: null };
    case 'FETCH_REPOSITORY_FILES_SUCCESS':
      return { ...state, files: action.payload, loading: false };
    case 'FETCH_REPOSITORY_FILES_FAILURE':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
};

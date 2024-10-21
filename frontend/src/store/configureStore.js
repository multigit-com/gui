import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import { repositoryReducer } from '../reducers/repositoryReducer';

const rootReducer = combineReducers({
  repository: repositoryReducer,
  // ... other reducers
});

const store = createStore(rootReducer, applyMiddleware(thunk));

export default store;

import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
} from "amazon-cognito-identity-js";

const poolData = {
  UserPoolId: process.env.REACT_APP_COGNITO_USER_POOL_ID || "",
  ClientId: process.env.REACT_APP_COGNITO_CLIENT_ID || "",
};

const userPool = new CognitoUserPool(poolData);

export const loginUser = (
  username: string,
  password: string,
  onSuccess: () => void,
  onFailure: (error: any) => void
) => {
  const user = new CognitoUser({ Username: username, Pool: userPool });
  const authDetails = new AuthenticationDetails({
    Username: username,
    Password: password,
  });

  user.authenticateUser(authDetails, { onSuccess, onFailure });
};

import React, { useState } from "react";
import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
} from "amazon-cognito-identity-js";
import Button from "../components/Button";
import Input from "../components/Input";

const poolData = {
  UserPoolId: "your-user-pool-id", // Replace with your AWS Cognito User Pool ID
  ClientId: "your-client-id", // Replace with your AWS Cognito App Client ID
};

const userPool = new CognitoUserPool(poolData);

const LoginScreen: React.FC<{ onLogin: () => void }> = ({ onLogin }) => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleLogin = () => {
    const authenticationDetails = new AuthenticationDetails({
      Username: username,
      Password: password,
    });

    const user = new CognitoUser({
      Username: username,
      Pool: userPool,
    });

    user.authenticateUser(authenticationDetails, {
      onSuccess: () => onLogin(),
      onFailure: () => setError("Invalid username or password"),
    });
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <Input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <Input
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button onClick={handleLogin} className="mt-4">
        Login
      </Button>
    </div>
  );
};

export default LoginScreen;

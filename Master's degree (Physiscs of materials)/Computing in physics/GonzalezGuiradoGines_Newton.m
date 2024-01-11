function y = Newton(f, fp, estimate)
  % Initialize the initial guess and convergence parameters
  x0 = estimate;     % Initial estimate of the root
  tolerance = 1e-6;  % Tolerance for convergence
  max_iterations = 100;  % Maximum number of iterations

  % Start a loop that performs iterations
  for i = 1:max_iterations
    f_x0 = f(x0);         % Evaluate the function at x0
    f_prime_x0 = fp(x0);  % Evaluate the derivative at x0

    % This checks if the derivative is too small to ensure convergence
    if abs(f_prime_x0) < tolerance
      disp("Derivative too small; convergence is not guaranteed.");
      break;   % Exit the loop if the derivative is too small
    end

    % Calculate a new approximation for the root using the Newton-Raphson formula
    x = x0 - (f_x0 / f_prime_x0);

    % Check if the difference between x and x0 is smaller than the tolerance
    % If so, it's considered that the method has converged
    if abs(x - x0) < tolerance
      y = x;    % Store the result in y
      fprintf("Converged to root %f in %d iterations.\n", y, i);
      return;   % Return the result and exit the function
    end

    % Update x0 with the new approximation
    x0 = x;
  end

  % If the loop completes all iterations without converging, display an error message
  fprintf("Newton-Raphson did not converge within the specified tolerance.");
  fprintf("Number of iterations = %d", max_iterations);
  y = NaN;  % Set the result to NaN to indicate that no valid root was found
end

% Define your functions
f = @(x) x - cos(x);
fp = @(x) 1 + sin(x);

estimate = 1.0;  % Initial estimate
Newton(f, fp, estimate);


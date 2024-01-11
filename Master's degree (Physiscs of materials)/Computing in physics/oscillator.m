function [x,t]  = oscillator(mass,damping,elastic_k)
  % Oscillator dynamics computed by Verlet's algorithm
  %   root    = oscillator(mass,damping,elastic_k)
  %
  %   mass = 1;  Kg            : oscillator mass
  %   damping = 0.1;  Kg/s     : damping coefficient
  %   elastic_k = 1;  N/m      : elastic constant

  % Initial conditions of the problem
  x0 = 1;  % Initial position
  v0 = 0;  % Initial velocity

  % Constants of the problem
  w0 = sqrt(elastic_k/mass);  % natural angular frequency
  betaNormalization = damping/(2*sqrt(elastic_k*mass));  % coefficient of the normalized EDO
  wNormalization =  sqrt(1 - (betaNormalization)^2);   % angular frequency of the normalized analytical solution in the underdamped case
  tau = 1/(betaNormalization*w0);  % Proper time of the damped harmonic oscillator
  tauNormalization = tau*w0;   % Proper time of the normalized damped harmonic oscillator
  TNormalization = 2*pi/wNormalization;   % Period of the normalized damped harmonic oscillator

  % Points with which I am going to represent the function
  n = 2001;

  % I create the time vector
  t = linspace(0, 12*TNormalization, n);

  % Step size
  h = t(2)-t(1);

  % Damping coefficient test to ensure that no overdamping behavior occurs
  if damping^2-4*elastic_k*mass>0
    error('The system is overdamped.');
  elseif damping^2-4*elastic_k*mass<0
    disp('The system is underdamped.');
  else
    error('The system is critical damping.');
  end

  % I create the position vector with the points that I want to represent the function
  x = zeros(1,n);

  % Initial conditions are assigned to the position vector
  x(1) = x0;
  x(2) = x0 + v0*h - (1/2)*(damping/(w0*mass)*v0 + x0)*h^2;   % Position after the initial position

  % Loop to calculate the positions through Verlet's method
  for k = 2:n-1
    x(k + 1) = ((2 - h^2)/(1+(h*betaNormalization)))*x(k) - ((1-(h*betaNormalization)) / (1+(h*betaNormalization)))*x(k-1);
  end


  % Functions to check that the numerical solution adjusts to the analytical solution
  f1 = exp(-t/tauNormalization);
  f2 = -exp(-t/tauNormalization);
  analytical_solution = exp(-t/tauNormalization).*cos(wNormalization*t);

  % Plot the position against normalized time
  figure;
  plot(t, x, 'b', 'LineWidth', 2);
  hold on;
  plot(t, f1, 'r', 'LineWidth', 1.5);
  plot(t, f2, 'r', 'LineWidth', 1.5);
  plot(t, analytical_solution, 'y', 'LineWidth', 2);
  hold off;
  xlabel('Normalized Time (t)');
  ylabel('Normalized position (x)');
  title('Oscillator Position vs. Normalized Time');
  legend('Numerical Solution', 'Amplitude Analytical Solution', 'Negative Amplitude Analytical Solution', 'Analytical solution');
  grid on;
return



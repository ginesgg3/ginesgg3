function x = gauss(A, b)
    % Se comprueba que la matriz es cuadrada para
    % que se pueda resolver por eliminación gaussiana
    [m, n] = size(A);
    if m ~= n
      error('Error: La matriz A debe ser cuadrada.');
    end

    % Se comprueba que en cada columna hay al menos un elemento no nulo
    % de forma que si no lo hay, no existe solucion unica
    % y se muestra el error en pantalla
    for i = 1:n
      for j = i:n
        if any(A(j,i) ~= 0)
          break; % Sale de este bucle interno si encuentra elemento no cero
        else
          error('El sistema no tiene solucion unica');
        end
      end
    end

    % Aumento la matriz A con los terminos independientes en Ab
    % para hacer los cambios de filas de forma mas rapida y eficiente
    Ab = [A, b];

    % Vector de ceros en el que se guarda el mayor coeficiente de cada fila
    s = zeros(1,n);

    % Bucle en el que se calculan los mayores coeficientes de cada fila
    for k = 1:n
      s(k) = max(abs(Ab(k,1:n)));
    end

    % Se inicia bucle para realizar la eliminacion gaussiana
    % con el el pivoteo parcial escalado
    for i = 1:n
      pivot_row = i; % fila pivote inicial
      max_scaled_element = abs(Ab(i,i))/s(i); % elemento maximo escalado inicial
      % Bucle para encontrar el elemento maximo escalado
      for j = i+1:n
        scaled_element = abs(Ab(j,i))/s(j);

        if scaled_element > max_scaled_element
          max_scaled_element = scaled_element;
          pivot_row = j;
        end
      end

      % Se intercambian las filas para poner la que tiene el mayor pivote
      % en la diagonal principal y, tambien, se intercambian los mayores
      % coeficientes guardados en s para la iteracion siguiente
      Ab([i,pivot_row],:) = Ab([pivot_row,i],:);
      s([i,pivot_row]) = s([pivot_row,i]);

      % Se eliminan los elementos debajo de la diagonal principal
      % restando la fila del pivote a las que estan debajo para
      % hacer cero los elementos debajo del pivote en cada iteracion
      for j = i+1:n
        factor = Ab(j,i)/Ab(i,i);
        Ab(j,i:end) = Ab(j,i:end) - factor * Ab(i,i:end);
      end
    end

    % Se comprueba si cualquier coeficiente de la diagonal principal es cero,
    % ya que, entonces el sistema de ecuaciones no tendria solucion unica
    % y no se podria resolver por este metodo
    if any(diag(A) == 0)
      error('Al menos un elemento de la diagonal principal es cero. No hay solución única.');
    end


    % Sustitucion hacia atras para obtener la solucion del sistema
    x = zeros(n, 1);
    for k = n:-1:1
      x(k) = (Ab(k,end) - sum(Ab(k,k+1:n) * x(k+1:n)))/Ab(k,k);
    end
end

% Ejemplo propuesto para comprobar la solucion del codigo:
A=[8 100; -1e-12 1e-12];
b=[8.0000000000001e15; -999.999999999999];

% Se muestra la solucion en pantalla:
format longE
x = gauss(A, b);
fprintf('Solución:\n');
disp(x);

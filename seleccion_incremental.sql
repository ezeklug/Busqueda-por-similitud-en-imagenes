CREATE OR REPLACE FUNCTION seleccion_incremental(k int, n int, a int) RETURNS int AS
$$
DECLARE
	i int;
	par record;
	valor1 NUMERIC(10,5);
	valor2 NUMERIC(10,5);
	promedio NUMERIC(10,5);
	diff NUMERIC(10,5);
	diff_max NUMERIC(10,5);
	p record;
	maximo double precision[];
	pivot record;
BEGIN
	DELETE FROM pivote;
	DROP TABLE IF EXISTS pares_objetos;
	create TEMPORARY table pares_objetos as SELECT i1.vector as vector1, i2.vector as vector2
					FROM imagenes i1, imagenes i2
					WHERE i1.id < i2.id
					ORDER BY random()
					LIMIT a;
	FOR i IN 1..k LOOP
		promedio:=0;
		RAISE NOTICE 'i %', i;
		DROP TABLE IF EXISTS promedios_pivotes;
		create TEMPORARY table promedios_pivotes(
			promedio NUMERIC(10,5),
			vector double precision[]
		);
						
		FOR p in (SELECT vector FROM imagenes WHERE vector NOT IN (SELECT vector1 FROM pares_objetos UNION SELECT vector2 FROM pares_objetos) ORDER BY random() LIMIT n) LOOP
			FOR par in (SELECT * FROM pares_objetos) LOOP
				valor1:=cosine_distance(p.vector, par.vector1);
				valor2:=cosine_distance(p.vector, par.vector2); 
				diff_max:=ABS(valor1-valor2);
				RAISE NOTICE 'DIFF %', diff_max;
				FOR pivot in (SELECT * FROM pivote) LOOP
				   valor1:=cosine_distance(pivot.vector, par.vector1);
				   valor2:=cosine_distance(pivot.vector, par.vector2);
			         diff:=ABS(valor1-valor2);
				   IF diff > diff_max THEN 
				       diff_max:=diff;
				   END IF;
				END LOOP;
				promedio:=promedio+diff_max;
			END LOOP;
			promedio:=promedio/a;
			
			INSERT INTO promedios_pivotes (promedio, vector) VALUES (promedio, p.vector);
		END LOOP;
		maximo:=(SELECT pivo1.vector FROM promedios_pivotes pivo1 WHERE  pivo1.promedio=(SELECT MAX(pivo.promedio) FROM promedios_pivotes pivo LIMIT 1) LIMIT 1);
		INSERT INTO pivote(id_pivote, nivel, vector) VALUES (i,i,maximo);
	END LOOP;
	RETURN 1;
END;
$$ LANGUAGE "plpgsql";

select * from seleccion_incremental(7,50,100)
select * from pivote
CREATE OR REPLACE FUNCTION histograma() RETURNS integer AS
$$
DECLARE
	p record;
	cantidad_intervalos NUMERIC;
	minimo NUMERIC;
	maximo NUMERIC;
	maximo_global NUMERIC;
	sup NUMERIC;
	inf NUMERIC;
	muestra NUMERIC;
	ni bigint;
	intervalo record;
BEGIN
	cantidad_intervalos=3;
	minimo=0;
	maximo_global=1;
	maximo=maximo_global;
	muestra=5000;
	DROP TABLE IF EXISTS histograma;
	CREATE TABLE histograma(intervalo numrange, nivel integer);
	DROP TABLE IF EXISTS distancias;
	create table distancias(
	id serial,
	vector1 double precision[],
	vector2 double precision[],
	distancia double precision);
	INSERT INTO distancias(vector1,vector2,distancia) SELECT i1.vector as vector1, i2.vector as vector2, 0 as distancia 
	FROM imagenes i1,imagenes i2
		WHERE i1.id<i2.id
		ORDER BY random()
		limit muestra;
		FOR p in (SELECT * FROM distancias) LOOP
			UPDATE public.distancias
				SET distancia=cosine_distance(p.vector1, p.vector2)
				WHERE vector1=p.vector1 AND vector2=p.vector2;
		END LOOP;
		inf = 0;
		INSERT INTO histograma(intervalo,nivel) VALUES (numrange(0,1,'[]'),0);
		FOR ni IN (SELECT nivel from pivote where nivel<>0) LOOP
			-- por cada pivote
			RAISE NOTICE 'nivel %', ni;
			FOR intervalo in (SELECT * from histograma where nivel=ni-1) LOOP
			minimo=lower(intervalo.intervalo);
			maximo=upper(intervalo.intervalo);
			RAISE NOTICE 'min % max %', minimo, maximo;
			inf=minimo;
				FOR i IN 1..cantidad_intervalos LOOP
					with distanciass as (select distancia, row_number() over (order by distancia) as position from distancias where distancia between minimo and maximo)
					select distancia into sup from distanciass where position=(((SELECT COUNT(*) FROM distanciass)/cantidad_intervalos)*i)::integer AND 
									(SELECT COUNT(*) FROM distanciass) > cantidad_intervalos;
					RAISE NOTICE 'sup %', sup;
					IF (sup is null) THEN
						sup=(((maximo-minimo)/cantidad_intervalos)*i)+minimo;
						RAISE NOTICE 'sup cambiado % inf %', sup, inf;
					END IF;
					IF (i = cantidad_intervalos) THEN
						sup=maximo;
					END IF;
					IF (sup = maximo_global) THEN
						INSERT INTO histograma(intervalo, nivel) VALUES (numrange(inf,sup,'[]'), ni);
					ELSE
						INSERT INTO histograma(intervalo, nivel) VALUES (numrange(inf,sup,'[)'), ni);
						inf=sup;
					END IF;
				END LOOP;
			END LOOP;
		END LOOP;
RETURN 1;
END;
$$ LANGUAGE "plpgsql";
SELECT * FROM histograma();
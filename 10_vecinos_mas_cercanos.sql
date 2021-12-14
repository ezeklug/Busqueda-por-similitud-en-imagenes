CREATE OR REPLACE FUNCTION diez_vecinos_mas_cercanos(img_vector double precision[], radio NUMERIC) RETURNS SETOF vecino AS
$$
DECLARE
	rec vecino;
	vec record;
	padres bigint[];
	distancia_p numeric;

BEGIN
	padres:=ARRAY(SELECT id_nodo FROM tree WHERE id_padre IS null);
	
	FOR vec IN (SELECT * FROM pivote ORDER BY id_pivote) LOOP
		distancia_p := cosine_distance(img_vector, vec.vector); --Calculamos la distancia del vector al pivote
		
		padres:= ARRAY(SELECT id_nodo FROM tree  
					   WHERE numrange(distancia_p-radio,distancia_p + radio, '[]') && intervalo_act
					   AND id_padre = ANY(padres)); 
	   RAISE NOTICE 'padres %', padres ;
	END LOOP;
	
	RETURN QUERY (SELECT id, path, id_hoja, web_path, cosine_distance(vector, img_vector) as distancia FROM imagenes  
				  WHERE id_hoja = ANY(padres) 
				  AND cosine_distance(vector, img_vector) <= radio 
				  ORDER BY distancia
				  LIMIT 10);
END;

$$ LANGUAGE "plpgsql"; 

CREATE TYPE vecino AS(
id integer,
path VARCHAR(255),
id_hoja bigint,
web_path VARCHAR(2083),
distancia double precision
);
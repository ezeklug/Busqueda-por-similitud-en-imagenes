create or replace function actualizar_arbol_update() RETURNS TRIGGER AS
$$
DECLARE
padre bigint;
padre_id bigint;
nodo_id bigint;
nodos_insertados  bigint[];
vec record;
cantidad_pivotes int;
inter_max numrange;
inter_act numrange;
distancia numeric;
minimo numeric;
maximo numeric;
BEGIN
	IF (SELECT COUNT(*) FROM imagenes WHERE id_hoja=OLD.id_hoja AND id <> OLD.id) = 0 THEN
		padre:=1;
		nodo_id :=(SELECT t.id_padre FROM tree t WHERE t.id_nodo=OLD.id_hoja);
		DELETE FROM tree t WHERE t.id_nodo=OLD.id_hoja;
		WHILE padre>0 LOOP
			IF (SELECT COUNT(*) FROM tree t WHERE t.id_padre=nodo_id) = 0 THEN
				padre_id := (SELECT t.id_padre FROM tree t WHERE t.id_nodo=nodo_id);
				DELETE FROM tree t WHERE t.id_nodo=nodo_id;
				nodo_id  := padre_id;
				IF nodo_id IS NULL THEN padre:=0;
				END IF;
			ELSE padre:= 0;
			END IF;
		END LOOP;
	END IF;

-- CREAR RAIZ
	IF (SELECT COUNT(*) FROM tree) = 0 THEN
		INSERT INTO tree(id_padre, nivel, intervalo_max, intervalo_act)
			VALUES(null, 0, numrange(0,1,'[]'), null);
	END IF;
	nodos_insertados:= ARRAY[(SELECT id_nodo from tree where id_padre is null)];
-- RECORRER PIVOTES
	FOR vec IN (SELECT vector, id_pivote FROM pivote ORDER BY id_pivote) LOOP	
		--SI EL NODO CON EL NIVEL DEL PIVOTE Y LA DISTANCIA NO ESTA EN EL ARBOL, SE CREA.
		distancia = cosine_distance(NEW.vector, vec.vector)::numeric;
		IF (SELECT COUNT(*) FROM tree 
			WHERE nivel=vec.id_pivote AND 
			distancia <@ intervalo_max
		   	AND id_padre = nodos_insertados[vec.id_pivote]) = 0 THEN
			inter_max=(SELECT intervalo FROM histograma WHERE nivel=vec.id_pivote AND distancia <@ intervalo);
			if (upper(inter_max) >= distancia+0.000000000000000001) THEN
				inter_act=numrange(distancia, distancia+0.000000000000000001, '[)');
			ELSif (lower(inter_max) <=distancia-0.000000000000000001) THEN
				inter_act=numrange(distancia-0.000000000000000001, distancia, '(]');
			END IF;
			if (inter_act is null) then
				RAISE NOTICE 'inter_act null en 34';
			END IF;
			INSERT INTO tree(id_padre,nivel, intervalo_max, intervalo_act)
				VALUES(nodos_insertados[vec.id_pivote], vec.id_pivote, inter_max, inter_act);
			nodos_insertados:= nodos_insertados || (SELECT lastval());
		ELSE nodos_insertados:= nodos_insertados || (SELECT id_nodo FROM tree 
													WHERE nivel=vec.id_pivote AND 
													distancia <@ intervalo_max
													AND id_padre = nodos_insertados[vec.id_pivote] limit 1);
			inter_act= (SELECT intervalo_act FROM tree 
					  WHERE nivel=vec.id_pivote AND distancia 
					  <@ intervalo_max AND id_padre = nodos_insertados[vec.id_pivote]);
			IF (lower(inter_act)>distancia) THEN
				inter_act=numrange(distancia,upper(inter_act), '[]');
			ELSEIF (upper(inter_act)<distancia) THEN
				inter_act=numrange(lower(inter_act),distancia,'[]');
			END IF;
			if (inter_act is null) then
				RAISE NOTICE 'inter_act null en 55';
			END IF;
			UPDATE tree SET intervalo_act = inter_act
				WHERE nivel=vec.id_pivote AND distancia <@ intervalo_max AND id_padre = nodos_insertados[vec.id_pivote];
		END IF;
	END LOOP;
	--actualizar intervalo actual de nodo raiz.
	maximo=(SELECT MAX(UPPER(intervalo_act)) FROM tree);
	minimo=(SELECT MIN(LOWER(intervalo_act)) FROM tree);
	inter_act = numrange(minimo,maximo,'[]');
	UPDATE tree SET intervalo_act = inter_act
		WHERE nivel=0;
	cantidad_pivotes:=(SELECT COUNT(*) FROM pivote);
	UPDATE imagenes
	SET id_hoja=nodos_insertados[cantidad_pivotes+1]
	WHERE id = NEW.id;
   RETURN NEW;
END;
$$ LANGUAGE "plpgsql"; 

CREATE TRIGGER fhqt_update
AFTER  UPDATE
ON imagenes
FOR EACH ROW
WHEN (NEW.vector <> OLD.vector)
EXECUTE PROCEDURE actualizar_arbol_update()




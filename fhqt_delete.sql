CREATE TRIGGER fhqt_delete
BEFORE DELETE
ON imagenes
FOR EACH ROW
EXECUTE PROCEDURE actualizar_arbol_delete();

create or replace function actualizar_arbol_delete() RETURNS TRIGGER AS
$$
DECLARE
padre bigint;
padre_id bigint;
nodo_id bigint;
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
	IF ((SELECT COUNT(*) FROM tree) = 1) THEN 
		DELETE FROM tree WHERE id_padre is null;
	END IF;
    RETURN OLD;
END;
$$ LANGUAGE "plpgsql"; 
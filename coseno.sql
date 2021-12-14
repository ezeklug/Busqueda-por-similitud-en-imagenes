--for calculation of norm vector --
CREATE or REPLACE FUNCTION public.vector_norm(IN vector double precision[])
    RETURNS double precision AS 
$BODY$
BEGIN
    RETURN(SELECT SQRT(SUM(pow)) FROM (SELECT POWER(e,2) as pow from unnest(vector) as e) as norm);
END;
$BODY$ LANGUAGE 'plpgsql'; 

--for caculation of dot_product--
CREATE OR REPLACE FUNCTION public.dot_product(IN vector1 double precision[], IN vector2 double precision[])
    RETURNS double precision    
AS $BODY$
BEGIN
    RETURN(SELECT sum(mul) FROM (SELECT v1e*v2e as mul FROM unnest(vector1, vector2) AS t(v1e,v2e)) AS denominator);
END;
$BODY$ LANGUAGE 'plpgsql';

--for calculatuion of cosine distance--
CREATE OR REPLACE FUNCTION public.cosine_distance(IN vector1 double precision[], IN vector2 double precision[])
	RETURNS double precision     
	LANGUAGE 'plpgsql'  
AS $BODY$ 
BEGIN    
	RETURN ((SELECT 1-((select public.dot_product(vector1, vector2) as dot_pod)/((select public.vector_norm(vector1) as norm1) * (select public.vector_norm(vector2) as norm2))) AS distance_value)); 
END; $BODY$;
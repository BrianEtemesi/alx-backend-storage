-- create procedure to compute and store average weighted score
--		for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN in_user_id INT
)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_weighted_score FLOAT;
    
    -- Calculate the total weighted score for the user
    SELECT SUM(corrections.score * projects.weight) INTO total_weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = in_user_id;
    
    -- Calculate the total weight for the user
    SELECT SUM(projects.weight) INTO total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = in_user_id;
    
    -- Calculate the average weighted score
    IF total_weight > 0 THEN
        SET average_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET average_weighted_score = 0;
    END IF;
    
    -- Update the average_score for the user
    UPDATE users
    SET average_score = average_weighted_score
    WHERE id = in_user_id;
END //

DELIMITER ;

-- creates a stored procedure that computes and store
--		the average score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN in_user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_corrections INT;
    DECLARE average_score FLOAT;
    
    -- Calculate the total score for the user
    SELECT SUM(score) INTO total_score
    FROM corrections
    WHERE user_id = in_user_id;
    
    -- Calculate the total number of corrections for the user
    SELECT COUNT(*) INTO total_corrections
    FROM corrections
    WHERE user_id = in_user_id;
    
    -- Calculate the average score
    IF total_corrections > 0 THEN
        SET average_score = total_score / total_corrections;
    ELSE
        SET average_score = 0;
    END IF;
    
    -- Update the average_score for the user
    UPDATE users
    SET average_score = average_score
    WHERE id = in_user_id;
END //

DELIMITER ;

-- average weighted score for all users
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_weighted_score FLOAT;

    -- Cursor to iterate through users
    DECLARE users_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN users_cursor;

    -- Loop through each user
    user_loop: LOOP
        -- Fetch the next user ID
        FETCH users_cursor INTO user_id;
        
        -- Exit the loop if no more users
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Calculate the total weighted score for the user
        SELECT SUM(corrections.score * projects.weight) INTO total_weighted_score
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Calculate the total weight for the user
        SELECT SUM(projects.weight) INTO total_weight
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Calculate the average weighted score
        IF total_weight > 0 THEN
            SET average_weighted_score = total_weighted_score / total_weight;
        ELSE
            SET average_weighted_score = 0;
        END IF;

        -- Update the average_score for the user
        UPDATE users
        SET average_score = average_weighted_score
        WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE users_cursor;
END //

DELIMITER ;

//go:build wasm

package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/conduitio/conduit-commons/opencdc"
	sdk "github.com/conduitio/conduit-processor-sdk"
)

func appearanceProcessor() {
	sdk.Run(sdk.NewProcessorFunc(
		sdk.Specification{Name: "appearance-processor", Version: "v1.0.0"},
		func(ctx context.Context, record opencdc.Record) (opencdc.Record, error) {
			// Get a logger instance
			logger := sdk.Logger(ctx).With().Str("processor", "appearance-processor").Logger()

			// Check if Payload.After is structured data
			payloadAfter, ok := record.Payload.After.(opencdc.StructuredData)
			if !ok {
				logger.Warn().Msg("Payload.After is not structured data, skipping record")
				return record, nil
			}

			// Log the raw payload for debugging
			payloadJSON, _ := json.Marshal(payloadAfter)
			logger.Info().Msgf("Raw Payload.After: %s", string(payloadJSON))

			// Extract appearance object
			appearance, ok := payloadAfter["appearance"].(map[string]interface{})
			if !ok {
				logger.Warn().Msg("No 'appearance' object found, skipping record")
				return record, nil
			}

			// Extract the fields from the appearance object
			mode := ""
			colorway := ""
			theme := ""
			deleted := false
			var deletedAt interface{} = nil // Default to nil

			if m, exists := appearance["mode"].(string); exists {
				mode = m
			}
			if c, exists := appearance["colorway"].(string); exists {
				colorway = c
			}
			if t, exists := appearance["theme"].(string); exists {
				theme = t
			}
			if d, exists := appearance["deleted"].(bool); exists {
				deleted = d
			}
			if da, exists := appearance["deleted_at"].(string); exists && da != "" {
				deletedAt = da // Only set a value if it's non-empty
			}

			// Get the profile ID from the 'id' field
			profileID, ok := payloadAfter["id"].(string)
			if !ok {
				logger.Error().Msg("id field not found in record")
				return record, fmt.Errorf("id field not found in record")
			}

			// Create a new payload with appearance fields
			newPayload := opencdc.StructuredData{
				"mode":       mode,
				"colorway":   colorway,
				"theme":      theme,
				"deleted":    deleted,
				"deleted_at": deletedAt, // Set to nil if not present
				"profile_id": profileID,
			}

			// Set the new payload in the record
			record.Payload.After = newPayload

			// Log the transformed record
			transformedPayloadJSON, _ := json.Marshal(newPayload)
			logger.Info().Msgf("Transformed Payload.After: %s", string(transformedPayloadJSON))

			// Return the modified record
			return record, nil
		},
	))
}

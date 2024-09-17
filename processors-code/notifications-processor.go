//go:build wasm

package main

import (
	"context"
	"strings"
	"time"

	"github.com/conduitio/conduit-commons/opencdc"
	sdk "github.com/conduitio/conduit-processor-sdk"
)

func main() {
	sdk.Run(sdk.NewProcessorFunc(
		sdk.Specification{Name: "notifications-processor", Version: "v1.0.0"},
		func(ctx context.Context, record opencdc.Record) (opencdc.Record, error) {
			// Get a logger instance
			logger := sdk.Logger(ctx).With().Str("processor", "notifications-processor").Logger()

			// Check if Payload.After is structured data
			payloadAfter, ok := record.Payload.After.(opencdc.StructuredData)
			if !ok {
				logger.Warn().Msg("Payload.After is not structured data, skipping record")
				return record, nil
			}

			// Extract notifications array
			notifications, ok := payloadAfter["notifications"].([]interface{})
			if !ok {
				logger.Warn().Msg("No 'notifications' array found, skipping record")
				return record, nil
			}

			// Function to check if a notification exists in the array
			checkNotifications := func(value string) bool {
				for _, n := range notifications {
					if nStr, ok := n.(string); ok && strings.EqualFold(nStr, value) {
						return true
					}
				}
				return false
			}

			// Map notifications to corresponding boolean fields
			newPayload := opencdc.StructuredData{
				"push_follows":    checkNotifications("Follows"),
				"push_comments":   checkNotifications("Comments"),
				"push_quotes":     checkNotifications("Quotes"),
				"push_likes":      checkNotifications("Likes"),
				"push_mentions":   checkNotifications("Mentions"),
				"push_tp_invites": checkNotifications("TeaPartyInvites"),
				"push_tp_replies": checkNotifications("TeaPartyReply"),

				"app_follows":    checkNotifications("Follows"),
				"app_comments":   checkNotifications("Comments"),
				"app_quotes":     checkNotifications("Quotes"),
				"app_likes":      checkNotifications("Likes"),
				"app_mentions":   checkNotifications("Mentions"),
				"app_tp_invites": checkNotifications("TeaPartyInvites"),
				"app_tp_replies": checkNotifications("TeaPartyReply"),

				"deleted":    false,              // Set default for deleted
				"deleted_at": time.Time{},        // Set deleted_at to empty
				"profile_id": payloadAfter["id"], // Profile ID from DynamoDB
			}

			// Log the transformed record
			logger.Info().Msgf("Transformed Payload.After: %#v", newPayload)

			// Set the new payload in the record
			record.Payload.After = newPayload

			// Return the modified record
			return record, nil
		},
	))
}
